require("dotenv").config();

const express = require("express");
const connectDB = require("./connectDB");

const app = express();

(async () => {
    await connectDB();

    app.use(express.json());

    const PORT = process.env.PORT;
    app.listen(PORT, () => {
        console.log(`Server starts on port ${PORT}`);
    });
})();