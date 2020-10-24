db = db.getSiblings('smart-dev')
db.createUser(
    {
        user: "admin",
        pwd: "password",
        roles: [
            {
                role: "readWrite",
                db: "smart-dev"
            }
        ]
    }
);