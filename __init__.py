import sys
from mycroft import MycroftSkill, intent_handler # type: ignore
sys.path.append("/usr/lib") # type: ignore
from UBUVoiceAssistant.util import util # type: ignore
from UBUVoiceAssistant.model.grade_item import GradeItem # type: ignore


class UbuGradesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.forums = {}
        self.learning = True

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler('Grades.intent')
    def handle_grades_intent(self, message):
        grades = self.ws.get_final_grades()
        self.speak(util.text_to_speech(grades))

    @intent_handler('CourseGrades.intent')
    def handle_course_grades(self, message):
        course = message.data['course']
        course_id = util.get_course_id_by_name(course, self.ws.get_user_courses())
        if course_id:
            course = self.ws.get_user().get_course(course_id)
            course_grades = course.get_grades()
            # If the course grades have never been looked up
            if not course_grades:
                course_grades = self.ws.get_course_grades(course_id)
                course_grades = [GradeItem(grade) for grade in course_grades['gradeitems']]
                course.set_grades(course_grades)

            course_grades = [str(grade) for grade in course_grades
                             if grade.get_type() == 'mod' and grade.get_value() is not None]
            self.speak(util.text_to_speech(course_grades))
        else:
            self.speak_dialog('no.course')


def create_skill():
    return UbuGradesSkill()
