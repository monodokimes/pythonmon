import jsonmanager
import component_module
import logger
import configuration
import input

from entity import Entity


class Scene:
    def __init__(self, name, entities_data):
        self.name = name
        self.entities = []
        self.event_input = None
        self.cont_input = None

        for entity_data in entities_data:
            position = (entity_data["X"], entity_data["Y"])

            entity = Entity(entity_data["Name"], position)
            for component_data in entity_data["Components"]:
                try:
                    component_constructor = getattr(component_module, component_data["Type"])
                    component = component_constructor()
                    component.scene = self

                    data = component_data["ComponentData"]
                    if not len(data) == 0:
                        component.load_data(data)

                    entity.add_component(component)
                except AttributeError:
                    logger.log(component_data["Type"] + " not recognised :/")

            self.entities.append(entity)

    def start(self):
        self.event_input = input.KeyboardInputType.NONE
        self.cont_input = input.KeyboardInputType.NONE

        for entity in self.entities:
            entity.start()

    def update(self, event_input, cont_input):
        self.event_input = event_input
        self.cont_input = cont_input
        for entity in self.entities:
            entity.update()

    def find_entity(self, entity_name):
        for entity in self.entities:
            if entity.name == entity_name:
                return entity
        return None


class SceneManager:
    @staticmethod
    def get_path(scene_name):
        return configuration.scene_data_folder_path + scene_name + '.json'

    @staticmethod
    def load_scene(scene_name):
        path = SceneManager.get_path(scene_name)
        scene_data = jsonmanager.get_data(path)

        return Scene(scene_name, scene_data['Entities'])

    @staticmethod
    def check_if_scene_exists(scene_name):
        path = SceneManager.get_path(scene_name)

        return jsonmanager.check_for_file(path)
