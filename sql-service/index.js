// server/index.js

import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import runSqlRoute from "./routes/runSql.js";

dotenv.config();

const app = express();
const port = process.env.PORT;

app.use(cors());
app.use(express.json());

// Routes
app.use("/", runSqlRoute);

app.listen(port, () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
});