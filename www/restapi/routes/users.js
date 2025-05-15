const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController");
const getUser = require("../middleware/getUser");

// get the list of users
router.get("/", userController.getAllUsers);

// add user
router.post("/", userController.createUser);

// get user with id
router.get("/:id", getUser, userController.getUserById);

router.put("/:id", getUser, userController.updateUser);

router.delete("/:id", getUser, userController.deleteUser);

module.exports = router;
