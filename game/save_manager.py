import logging

from utility.file import JsonFile, JkrFile

class SaveManager:
    def __init__(self, sim):
        self.__setLoggers__()
        self.sim = sim

    def __setLoggers__(self):
        # Set logger for current object
        self.logger = logging.getLogger(__name__)

    def saveGameState(self, file_name):
        self.logger.info("Trying to save data to file...")

        file_manager = JsonFile(file_name)
        game_state_export = self.sim.toDict()
        saved_filename = file_manager.write(game_state_export)

        if saved_filename is not None:
            self.logger.info(F"Finished saving game state")
        else:
            self.logger.error("Issue occured while trying to save the game state")
            return False
        
        return True

    def loadGameState(self, file_name):
        self.logger.info("Trying to load data from file...")

        file_manager = JsonFile(file_name)
        game_state_export = file_manager.read()
        
        if game_state_export is not None:
            self.sim.fromDict(game_state_export)
            self.logger.info("Finished loading game state")
        else:
            self.logger.error("Issue occured while trying to load the game state")
            return False

        return True

    def importGameState(self, file_name):
        self.logger.info("Trying to import data from game save file")

        file_manager = JkrFile(file_name)
        save_export = file_manager.read()

        if save_export is not None:
            self.sim.fromSave(save_export)
            self.logger.info("Finished importing game state")
        else:
            self.logger.error("Issue occured while trying to load the game state")
            return False

        return True