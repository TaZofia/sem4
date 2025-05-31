const User = require("../models/user");

const bcrypt = require("bcrypt");
const jwt = require('jsonwebtoken');

const SECRET_KEY = process.env.JWT_SECRET;

// req - it is request which sends client to server
// res - server's response

exports.getAllUsers = async function (req, res) {

    let isAdmin;
    isAdmin = req.userRole === 'admin';

    if (!isAdmin) {
        return res.status(403).json({ message: "Forbidden: Only admin can see all the users!" });
    }

    try {
        const users = await User.find().select("-password")
        res.json(users)
    } catch (err) {
        res.status(500).json({message: err.message})
    }
}

exports.createUser = async function (req, res) {
    try {
        const { username, email, password } = req.body;

        if (!username || !email || !password) {
            return res.status(400).json({ message: "Username, email and password are required" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const user = new User({
            username,
            email,
            password: hashedPassword,
            role: 'user',  // we can create only users
        });

        const newUser = await user.save();

        res.status(201).json({ newUser });
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
}

exports.getUserById = async function (req, res) {
    res.json(req.user)
}

exports.updateUser = async function (req, res) {

    let isAdmin;
    isAdmin = req.userRole === 'admin';

    // when non admin user tries to update any other user - forbidden
    if (!isAdmin && req.userId !== res.user._id.toString()) {
        return res.status(403).json({ message: "Forbidden: You can only update your own account" });
    }

    // when admin tries to update other admin - forbidden
    if (isAdmin && res.user.role === 'admin' && req.userId !== res.user._id.toString()) {
        return res.status(403).json({ message: "Forbidden: Admins cannot edit other admins" });
    }

    // we assume that is already in res.user (was loaded by middleware)
    try {
        // we can update only this parts which we've got in req.body
        if (req.body.username != null) {
            res.user.username = req.body.username;
        }
        if (req.body.email != null) {
            res.user.email = req.body.email;
        }
        if (req.body.password != null) {
            res.user.password = await bcrypt.hash(req.body.password, 10);
        }
        if (req.body.role != null) {
            if (isAdmin) {
                res.user.role = req.body.role;
            } else {
                // user can't change its role !never!
                return res.status(403).json({ message: "Forbidden: Only admins can change roles" });
            }
        }
        const updatedUser = await res.user.save();
        res.json(updatedUser);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
}

exports.deleteUser = async function (req, res) {

    let isAdmin;
    isAdmin = req.userRole === 'admin';

    // when non admin user tries to delete any other user - forbidden
    if (!isAdmin && req.userId !== res.user._id.toString()) {
        return res.status(403).json({ message: "Forbidden: You can only delete your own account" });
    }

    // when admin tries to delete other admin - forbidden
    if (isAdmin && res.user.role === 'admin' && req.userId !== res.user._id.toString()) {
        return res.status(403).json({ message: "Forbidden: Admins cannot delete other admins" });
    }

    try {
        await res.user.remove();
        res.json({ message: "User deleted" });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
}

exports.loginUser = async function (req, res) {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ message: "Username and password are required" });
    }

    try {
        const user = await User.findOne({ username });
        if (!user) {
            return res.status(401).json({ message: "Invalid username or password" });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        // wrong password
        if (!isMatch) {
            return res.status(401).json({ message: "Invalid username or password" });
        }

        const token = jwt.sign(
            { id: user._id, role: user.role },
            SECRET_KEY,
            {
                algorithm: "HS512",
                expiresIn: "2h" }
        );

        res.json({ token });

    } catch (err) {
        console.error("Login error:", err);
        res.status(500).json({ message: "Server error, please try again later" });
    }
}

// get a data from user whose id was in the token
exports.getLoggedInUser = async function (req, res) {
    try {
        const user = await User.findById(req.userId).select("-password"); // delete password from response
        if (!user) return res.status(404).json({ message: "User not found" });

        res.json(user);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
}

