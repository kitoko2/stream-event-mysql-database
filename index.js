const mysql = require("mysql");
const MySQLEvents = require("@rodrigogs/mysql-events");



const program = async () => {
    const connection = mysql.createConnection({
        host: "localhost",
        user: "root",
        password: "",
    });

    const instance = new MySQLEvents(connection, {
        startAtEnd: true,
        excludedSchemas: {
            mysql: true,
        },
    });

    await instance.start();

    instance.addTrigger({
        name: "lta_database",
        expression: "lta_database.etudiants",
        statement: MySQLEvents.STATEMENTS.ALL,
        onEvent: (event) => {
            // You will receive the events here
            console.log("Hellloo")
            console.log(event);
        },
    });

    instance.on(MySQLEvents.EVENTS.CONNECTION_ERROR, console.error);
    instance.on(MySQLEvents.EVENTS.ZONGJI_ERROR, console.error);
};

program()
    .then(() => console.log("Waiting for database events..."))
    .catch(console.error);