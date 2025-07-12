// sql-service/routes/runIdsSql.js

import express from "express";
const router = express.Router();
import createIdsSqlQuery from "../utils/createIdsSql.js";
import pool from "../db/pool.js";
import isSafeSql from "../utils/validateSql.js";

router.post("/run-ids-sql-query", async (req, res) => {
    try {
        const { entries } = req.body;

        if (!Array.isArray(entries) || entries.length === 0) {
            return res.status(400).json({ error: "Invalid entries array" });
        }

        const sqlQuery = createIdsSqlQuery(entries);

        if (!isSafeSql(sqlQuery)) {
            return res.status(400).json({ error: "Unsafe or disallowed SQL query." });
        }

        const allResults = [];
        const result = await pool.query(sqlQuery);
        allResults.push({ query: sqlQuery, rows: result.rows });
        res.json({ results: allResults });
    } catch (error) {
        console.error("Error running ID-based SQL query:", error);
        res.status(500).json({ error: "Internal server error" });
    }
});

export default router;
