import cmd

#globals
#costs in dollars
rent = 150
groceries = 50
#allowable time between events.
meal_interval = 6 #hours
sleep_interval = 16 #hours
exercise_interval = 2 #days
social_interval = 2 #days

class Character:
    def __init__(self):
        #out of 100
        self.base_mood = 80
        #out of 100
        self.base_energy = 80
        #In whole numbers of dollars
        self.money = 200
        #in hours
        self.last_meal = 14
        #in hours
        self.last_sleep = 0
        #in days
        self.last_exercise = 1
        #in days
        self.last_social = 1
        #number of meals
        self.groceries = 21
        self.hours_played = 8

    def add_hours(self, hours):
        #if we crossed a day boundary
        if (self.hours_played / 24) < ((self.hours_played + hours) / 24):
            self.last_exercise = self.last_exercise + 1
            self.last_social = self.last_social + 1
        self.last_meal = self.last_meal + hours
        self.last_sleep = self.last_sleep + hours
        self.hours_played = self.hours_played + hours

    def get_mood(self):
        mood = self.base_mood
        if self.last_meal > meal_interval:
            mood = mood - 10 * (self.last_meal - meal_interval)
        if self.last_exercise > exercise_interval:
            mood = mood - 10 * (self.last_exercise - exercise_interval)
        if self.last_social > social_interval:
            mood = mood - 10 * (self.last_social - social_interval)
        return mood

    def get_energy(self):
        energy = self.base_energy
        if self.last_meal > meal_interval:
            energy = energy - 10 * (self.last_meal - meal_interval)
        if self.last_sleep > sleep_interval:
            energy = energy - 10 * (self.last_sleep - sleep_interval)
        if self.last_exercise > exercise_interval:
            energy = energy - 10 * (self.last_exercise - exercise_interval)
        return energy

    def work(self, hours):
        self.add_hours(hours)
        self.money = self.money + 10 * hours
        self.base_energy = self.base_energy - 5 * hours
        self.base_mood = self.base_mood - 5 * hours

    def sleep(self, hours):
        self.add_hours(hours)
        if hours < 4:
            return
        if hours > 8:
            hours = 8
        self.last_sleep = 0
        self.base_energy = 10 * hours
        if hours > 6:
            self.base_energy = self.base_energy + 20

    def eat(self):
        self.add_hours(1)
        self.last_meal = 0
        self.groceries = self.groceries - 1

    def exercise(self):
        self.add_hours(1)
        self.last_exercise = 0
        self.base_mood = self.base_mood + 5
        self.base_energy = self.base_energy - 5

    def shopping(self):
        self.add_hours(1)
        self.money = self.money - 50
        self.groceries = self.groceries + 21
        if self.groceries > 42:
            self.groceries = 42

    def game(self, hours):
        self.add_hours(hours)
        #fix this later to track hours spent gaming per day
        if hours > 4:
            hours = 4
        self.base_mood = self.base_mood + 5 * hours

    def hang_out(self, hours):
        self.add_hours(hours)
        self.money = self.money - 10 * hours
        self.base_energy = self.base_energy - 5 * hours
        if hours > 3:
            hours = 3
        self.base_mood = self.base_mood + 10 * hours
        self.last_social = 0

class Sdabto_Cmd(cmd.Cmd):
    intro = '''Welcome to Some Days Are Better Than Others
Trigger Warning: Suicide
Type 'help' or '?' for some suggestions of what to do.\n'''
    prompt = 'What would you like to do? '

    def __init__(self, character):
        super(Sdabto_Cmd, self).__init__()
        self.character = character

    def preloop(self):
        pass

    def postloop(self):
        print("Goodbye")

    def default(self, line):
        print("Sorry, that command is not recognized.  Try 'help' or '?' for suggestions")

    def do_exit(self, arg):
        '''Exit the program'''
        return True

    def do_quit(self, arg):
        '''Exit the program'''
        return True

    def do_status(self, arg):
        '''Return your vital statistics'''
        mood = self.character.get_mood()
        energy = self.character.get_energy()
        day = (self.character.hours_played // 24) + 1
        hour = self.character.hours_played % 24
        print("Day: " + str(day) + " Hour: " + str(hour) + " Mood: " + str(mood) +\
                " Energy: " + str(energy) + " Money: $" + str(self.character.money) +\
                " Food: " + str(self.character.groceries) + " meals")
        #for debugging
        print("last_meal: "  + str(self.character.last_meal))
        print("last_sleep: "  + str(self.character.last_sleep))
        print("last_exercise: "  + str(self.character.last_exercise))
        print("last_social: "  + str(self.character.last_social))

def main():
    Sdabto_Cmd(Character()).cmdloop()

if __name__ == '__main__':
    main()
