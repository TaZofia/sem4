const jwt = require("jsonwebtoken");

function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN - from header

    if (!token) return res.sendStatus(401); // Unauthorized

    // verify token using JWT_SECRET
    jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
        if (err) return res.sendStatus(403); // Forbidden
        req.userId = decoded.id;
        req.userRole = decoded.role;
        next();
    });
}

module.exports = authenticateToken;