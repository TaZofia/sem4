const User = require("../models/user");

exports.getAllUsers = async function (req, res) {
    try {
        const users = await User.find()
        res.json(users)
    } catch (err) {
        res.status(500).json({message: err.message})
    }
};

exports.createUser = async function (req, res) {
    const user = new User({
        username: req.body.username,
        email: req.body.email,
        password: req.body.password,
        role: req.body.role,
    });
    try {
        const newUser = await user.save();
        res.status(201).json({newUser});
    } catch (err) {
        res.status(400).json({message: err.message})
    }
};

exports.getUserById = async function (req, res) {
    res.json(req.user)
};

exports.updateUser = async function (req, res) {
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
            res.user.password = req.body.password;
        }
        if (req.body.role != null) {
            res.user.role = req.body.role;
        }
        const updatedUser = await res.user.save();
        res.json(updatedUser);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
};

exports.deleteUser = async function (req, res) {
    try {
        await res.user.remove();
        res.json({ message: "User deleted" });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};
