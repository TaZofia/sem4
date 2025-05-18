const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController");
const getUser = require("../middleware/getUser");
const authenticateToken = require("../middleware/auth");

// order of endpoints is important
// get the list of users
router.get("/", userController.getAllUsers);

// add user
router.post("/", userController.createUser);

// /users/me – already logged user
router.get("/me", authenticateToken, userController.getLoggedInUser);

// get user with id
router.get("/:id", getUser, userController.getUserById);

router.put("/:id", getUser, userController.updateUser);

router.delete("/:id", getUser, userController.deleteUser);

// login
router.post("/login", userController.loginUser);

module.exports = router;
