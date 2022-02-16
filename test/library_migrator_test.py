from db_controller.db_controller import DBController
from library_migrator.book_migrator import BookMigrator
from library_migrator.equipment_migrator import EquipmentMigrator


def testLibraryMigrator(bookDB: DBController, equipmentDB: DBController, newDB: DBController) -> None:
    testBookMigrator(bookDB, newDB)
    testEquipmentMigrator(equipmentDB, newDB)


def testBookMigrator(bookDB: DBController, newDB: DBController) -> None:
    bookMigrator = BookMigrator()
    bookMigrator.setOldDBController(bookDB)
    bookMigrator.setNewDBController(newDB)

    bookMigrator.addBookDepartment(0, 1)
    bookMigrator.addBookDepartment(1, 2)
    bookMigrator.addBookDepartment(2, 3)
    bookMigrator.addBookDepartment(3, 4)
    bookMigrator.addBookDepartment(4, 5)
    bookMigrator.addBookDepartment(9, 6)

    bookMigrator.migrateBook()


def testEquipmentMigrator(equipmentDB: DBController, newDB: DBController) -> None:

    equipmentMigrator = EquipmentMigrator()
    equipmentMigrator.setOldDBController(equipmentDB)
    equipmentMigrator.setNewDBController(newDB)

    equipmentMigrator.migrateEquipment()


if __name__ == "__main__":
    bookDB = DBController()
    bookDB.setDBName("Library2")
    bookDB.setDB()

    equipmentDB = DBController()
    equipmentDB.setDBName("Library")
    equipmentDB.setDB()

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    testLibraryMigrator(bookDB, equipmentDB, newDB)
