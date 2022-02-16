from db_controller.db_controller import DBController
from test.category_mapper_test import testCategoryMapper
from test.extra_vars_inserter_test import testExtraVarsInserter
from test.html_content_cleaner_test import testHtmlContentCleaner
from test.migrator_sql_test import testMigratorSql
from test.group_seperator_test import testGroupSeperator
from test.library_migrator_test import testLibraryMigrator

oldDB = DBController()
oldDB.setDBName("keeper_copy")
oldDB.setDB()

bookDB = DBController()
bookDB.setDBName("Library2")
bookDB.setDB()

equipmentDB = DBController()
equipmentDB.setDBName("Library")
equipmentDB.setDB()

newDB = DBController()
newDB.setDBName("keeper_new")
newDB.setDB()

testExtraVarsInserter(oldDB)
testHtmlContentCleaner(oldDB)
testCategoryMapper(oldDB)

testMigratorSql(newDB)

testGroupSeperator(oldDB, newDB)
testLibraryMigrator(bookDB, equipmentDB, newDB)
