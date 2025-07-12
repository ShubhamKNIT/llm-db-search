// sql-service/routes/runIdsSql.js

import express from "express";
import createIdsSqlQuery from "../utils/createIdsSql.js";
import dotenv from "dotenv";

dotenv.config();

const router = express.Router();

router.post("/run-ids-sql-query", async (req, res) => {
    try {
        const entries = req.body;

        if (!entries || typeof entries !== "object" || Object.keys(entries).length === 0) {
            return res.status(400).json({ error: "Invalid entries object." });
        }

        // Generate SQL queries for each table
        const sqlQueries = createIdsSqlQuery(entries);
        console.log("📜 Generated SQL queries:", sqlQueries);

        if (!sqlQueries || sqlQueries.length === 0) {
            return res.status(400).json({ error: "No valid SQL queries generated." });
        }

        // Send the SQL to /run-sql endpoint
        const fetchResponse = await fetch(process.env.RUN_SQL_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sql: sqlQueries }),  // Send as string
        });

        if (!fetchResponse.ok) {
            const text = await fetchResponse.text();
            console.error("⚠️ /run-sql response not OK:", text);
            return res.status(500).json({ error: "Failed to fetch SQL results from /run-sql." });
        }

        const result = await fetchResponse.json();
        return res.json(result);

    } catch (error) {
        console.error("❌ Error running ID-based SQL query:", error);
        return res.status(500).json({ error: "Internal server error." });
    }
});

export default router;
