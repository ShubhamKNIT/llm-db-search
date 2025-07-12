// sql-service/utils/createIdsSql.js

function createIdsSqlQuery(ids) {
    const ids = entries.map(e => e.id).filter(id => Number.isInteger(id));
    const idList = ids.join(", ");

    return `
        SELECT * FROM products
        WHERE id IN (${idList})
    `.trim();
}

export default createIdsSqlQuery;
