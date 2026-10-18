BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "group_problems_links" (
	"id"	INTEGER NOT NULL,
	"group_id"	INTEGER NOT NULL,
	"problem_id"	INTEGER NOT NULL,
	"deadline"	DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY("group_id") REFERENCES "groups"("id"),
	FOREIGN KEY("problem_id") REFERENCES "problems"("id")
);
CREATE TABLE IF NOT EXISTS "groups" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(30) NOT NULL,
	"invite_code"	VARCHAR(16) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("invite_code")
);
CREATE TABLE IF NOT EXISTS "problems" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(120) NOT NULL,
	"description"	TEXT,
	"difficulty"	VARCHAR(30) NOT NULL,
	"topic_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("topic_id") REFERENCES "topics"("id")
);
CREATE TABLE IF NOT EXISTS "reviews" (
	"id"	INTEGER NOT NULL,
	"status"	VARCHAR(9) NOT NULL,
	"comment"	TEXT NOT NULL,
	"submission_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("submission_id") REFERENCES "submissions"("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "submissions" (
	"id"	INTEGER NOT NULL,
	"input_code"	TEXT NOT NULL,
	"status"	VARCHAR(8) NOT NULL,
	"send_time"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"speed"	INTEGER,
	"memory"	INTEGER,
	"notes"	TEXT,
	"user_id"	INTEGER NOT NULL,
	"problem_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("problem_id") REFERENCES "problems"("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "tests" (
	"id"	INTEGER NOT NULL,
	"input_data"	TEXT NOT NULL,
	"output_data"	TEXT NOT NULL,
	"is_hidden"	BOOLEAN NOT NULL,
	"problem_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("problem_id") REFERENCES "problems"("id")
);
CREATE TABLE IF NOT EXISTS "topics" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(60) NOT NULL,
	"first_name"	VARCHAR(30) NOT NULL,
	"middle_name"	VARCHAR(30),
	"last_name"	VARCHAR(30) NOT NULL,
	"role"	VARCHAR(9) NOT NULL,
	"password_hash"	TEXT NOT NULL,
	"group_id"	INTEGER,
	UNIQUE("email"),
	PRIMARY KEY("id"),
	FOREIGN KEY("group_id") REFERENCES "groups"("id")
);
INSERT INTO "group_problems_links" VALUES (1,1,1,NULL);
INSERT INTO "groups" VALUES (1,'TESTGROUP','TESTCODE');
INSERT INTO "problems" VALUES (1,'Сортировка пузырьком','Описание','EASY',1);
INSERT INTO "problems" VALUES (2,'Сортировка log(n)','Лучше чем n!','EASY',1);
INSERT INTO "topics" VALUES (1,'Сортировка');
INSERT INTO "users" VALUES (1,'test@email.com','TEST_NAME',NULL,'TEST_LAST_NAME','STUDENT','TESTHASH',1);
INSERT INTO "users" VALUES (2,'teacher@email.com','TEACHER_NAME',NULL,'TEACHER_LAST_NAME','TEACHER','TESTHASH',NULL);
COMMIT;
