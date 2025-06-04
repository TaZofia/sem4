const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController");
const getUser = require("../middleware/getUser");
const authenticateToken = require("../middleware/auth");

// order of endpoints is important
// get the list of users
router.get("/", authenticateToken, userController.getAllUsers);

// add user - for everyone, auth not needed
router.post("/", userController.createUser);

// /users/me – already logged user
router.get("/me", authenticateToken, userController.getLoggedInUser);

router.get("/me/reviews", authenticateToken, userController.getMyReviews)

// get user with id
router.get("/:id", getUser, authenticateToken, userController.getUserById);

router.put("/:id", getUser, authenticateToken, userController.updateUser);

router.delete("/:id", getUser, authenticateToken, userController.deleteUser);

// login - for everyone
router.post("/login", userController.loginUser);

module.exports = router;
