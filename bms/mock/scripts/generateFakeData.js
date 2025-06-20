const fs = require("fs");
const path = require("path");
const jsf = require("json-schema-faker");

(async () => {
    const schemaFile = process.argv[2];
    if (!schemaFile) {
        console.error("Schema file path required");
        process.exit(1);
    }

    const absolutePath = path.resolve(schemaFile);
    const baseDir = path.dirname(absolutePath);

    try {
        process.chdir(baseDir);
        const schema = JSON.parse(fs.readFileSync(absolutePath, "utf8"));
        const fakeData = await jsf.resolve(schema);
        console.log(JSON.stringify(fakeData)); // no indent, no logging
    } catch (error) {
        console.error(error.message);
        process.exit(1);
    }
})();
