from abc import ABCMeta, abstractmethod
from typedef.typedef import Row, Table
from db_controller.db_controller import DBController


class LibraryMigrator(metaclass=ABCMeta):
    oldDBController: DBController
    newDBController: DBController

    oldTableMigrate: str
    newTableMigrate: str

    selectLibraryFormat = ("SELECT number, name, author"
                           " FROM {oldTableMigrate};")

    insertLibraryFormat: str

    @abstractmethod
    def __init__(self,
                 oldTableMigrate: str,
                 newTableMigrate: str) -> None:

        self.oldTableMigrate = oldTableMigrate
        self.newTableMigrate = newTableMigrate

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def migrateLibrary(self) -> None:
        libraryTable = self.selectLibrary()
        editedLibraryTable = self.getEditedLibraryTable(libraryTable)
        self.insertLibrary(editedLibraryTable)

    def selectLibrary(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.formatSelectLibraryQuery())
        libraryTable = cursor.fetchall()
        return libraryTable

    def formatSelectLibraryQuery(self) -> str:
        return self.selectLibraryFormat.format(oldTableMigrate=self.oldTableMigrate)

    def getEditedLibraryTable(self, libraryTable: Table) -> Table:
        editedLibraryTable: Table = list()

        for row in libraryTable:
            name = self.getLibraryName(row["name"])
            bookEquipmentIndex = self.findLibrary(editedLibraryTable, name)

            if(bookEquipmentIndex == -1):
                editedLibraryTable.append(self.editLibraryRow(row))
            else:
                editedLibraryTable[bookEquipmentIndex]["total"] += 1
                editedLibraryTable[bookEquipmentIndex]["enable"] += 1

        return editedLibraryTable

    @abstractmethod
    def getLibraryName(self, name: str) -> str: pass

    def findLibrary(self, table: Table, name: str) -> int:

        for i in range(len(table)-1, -1, -1):
            if(table[i]["name"] == name):
                return i
        return -1

    @abstractmethod
    def editLibraryRow(self, row: Row) -> Row: pass

    def setNameTotalOnRow(self, row: Row) -> Row:
        row["name"] = self.getLibraryName(row["name"])
        row["total"] = 1
        row["enable"] = 1
        return row

    def insertLibrary(self, editedLibraryTable: Table) -> None:
        cursor = self.newDBController.getCursor()

        cursor.executemany(
            self.formatInsertLibraryQuery(),
            editedLibraryTable
        )
        self.newDBController.getDB().commit()

    def formatInsertLibraryQuery(self) -> str:
        return self.insertLibraryFormat.format(newTableMigrate=self.newTableMigrate)
