const mongoose = require("mongoose");

async function connectDB() {
    try {
        await mongoose.connect(process.env.DATABASE_URL, {
            useNewUrlParser: true,      // new parser, mongoose 5 >
        });
        console.log("Connected successfully");
    } catch (error) {
        console.error("Error", error);
        process.exit(1);
    }
}

module.exports = connectDB;
