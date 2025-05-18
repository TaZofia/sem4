// run mongo:
// mongod --dbpath "K:\Program Files\MongoDB\Server\8.0\data"

require("dotenv").config();

const express = require("express");
const connectDB = require("./connectDB");

const app = express();

(async () => {
    await connectDB();

    app.use(express.json());

    // connect user's router so express would know how to handle endpoints
    const userRouter = require("./routes/users");
    app.use("/users", userRouter);

    const productsRouter = require("./routes/products");
    app.use("/products", productsRouter);

    const reviewsRouter = require("./routes/reviews");
    app.use("/reviews", reviewsRouter);

    const PORT = process.env.PORT;
    app.listen(PORT, () => {
        console.log(`Server starts on port ${PORT}`);
    });
})();