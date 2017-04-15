var mongo	= require("mongodb").MongoClient;
var nconf	= require("nconf");

nconf.argv().env();

let db;

mongo.connect(`mongodb://localhost:27017/blundertale`)
	.then((d) => {
		db = d;
		return db.authenticate(nconf.get("MONGO_USER"), nconf.get("MONGO_PASS"));
	})
	.then(() => {
		return db.createCollection("games");
	})
	.catch((err) => {
		console.error("[DB] DB connection failed", err);
	})
	.then(() => {
		db.close();
	});