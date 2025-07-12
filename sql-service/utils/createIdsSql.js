// sql-service/utils/createIdsSql.js

function createIdsSqlQuery(entries) {
    const allowedTables = ["laptops", "mobiles"];
    let sqlQueries = "";
    const tableIds = {};
    Object.entries(entries).forEach(([entry, tables]) => {
        // console.log(`Processing entry: ${entry}`);
        Object.entries(tables).forEach(([table, records]) => {
            // console.log(`Processing table: ${table}`);
            Object.values(records).forEach(record => {
                // console.log(`Record ID: ${record.id}, Distance: ${record.distance}`);
                if (!tableIds[table]) {
                    tableIds[table] = [];
                }
                tableIds[table].push(record.id);
            });
        });
    });

    Object.entries(tableIds).forEach(([table, ids]) => {
        if (allowedTables.includes(table)) {
            const idList = ids.join(", ");
            sqlQueries += `SELECT * FROM ${table} WHERE id IN (${idList});`;
        }
    });

    return sqlQueries;
}

export default createIdsSqlQuery;
