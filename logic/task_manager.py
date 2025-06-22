import os
from enum import IntEnum


class Task:
    def __init__(self, task, is_completed=False):
        self.task = task
        self.is_completed = is_completed

    def mark_completed(self):
        self.is_completed = True

    def __str__(self):
        status = '✅ Completed' if self.is_completed else '❌ Unfinished'
        return f'{self.task} is {status}'


class TaskManager:
    def __init__(self):
        self.task_list = []

    def add_task(self, task_name):
        task = Task(task_name)
        self.task_list.append(task)
        print('\nTask was added to list. \n')

    def complete_task(self, task_name):
        for task in self.task_list:
            if task.task == task_name:
                task.mark_completed()
                print('\nTask status was changed. \n')
                break

        else:
            print('This task was not found on the list.')
            choice = input('Would you like to add it? y/n \n')
            if choice == 'y':
                self.add_task(task_name)

    def show_list(self):
        if self.task_list:
            print('\nTASK LIST:')
            for task in self.task_list:
                print(task)
        else:
            print('\nList is empty')
        print('\n')

    def remove_from_list(self, task_name):
        for task in self.task_list:
            if task.task == task_name:
                self.task_list.remove(task)
                print(f'\nTask {task.task} removed from list. \n')
                break
        else:
            print('\nTask is not on the list.\n')

    def list_of_completed_tasks(self):
        if self.task_list:
            print('\nList of completed tasks:')
            for task in self.task_list:
                if task.is_completed == True:
                    print(task)
        else:
            print('\nList is empty\n')

    def list_of_unfinished_tasks(self):
        if self.task_list:
            for task in self.task_list:
                if task.is_completed == False:
                    print(task)
        else:
            print('\nList is empty\n')

    def save_list(self):
        try:
            file_path = os.path.dirname(__file__)
            path = os.path.join(file_path, 'task_list.txt')

            with open(path, 'w', encoding='UTF-8') as file:
                for task in self.task_list:
                    file.write(f"{task.task}|{task.is_completed}\n")
            print("\nList was saved\n")
        except Exception as e:
            print(f'\nFile was not saved: {e}')

    def load_list(self):
        try:
            file_path = os.path.dirname(__file__)
            path = os.path.join(file_path, 'task_list.txt')
            # file name or directory can be changed

            with open(path, 'r', encoding='UTF-8') as file:
                self.task_list.clear()
                for line in file:
                    name, status = line.strip().split('|', 1)
                    task = Task(name)
                    if status == 'True':
                        task.mark_completed()
                    self.task_list.append(task)
                print('\nFile loaded\n')
        except Exception as e:
            print(f'\nCould not load file: {e}')


class Menu(IntEnum):
    ADD_TASK = 1
    COMPLETE_TASK = 2
    SHOW_LIST = 3
    REMOVE_TASK = 4
    SHOW_LIST_OF_COMPLETED_TASKS = 5
    SHOW_LIST_OF_UNFINISHED_TASKS = 6
    SAVE_LIST = 7
    LOAD_LIST = 8
    END = 9
