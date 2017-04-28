import os
import shutil
import time


class Scan:

    def __init__(self, source, destination):
        print("Init: %s to %s" % (source, destination))
        self.source_dir = os.path.abspath(source)
        self.destination_dir = os.path.abspath(destination)
        self.start_time_seconds = time.time()
        self.start_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        self.visited_files = []
        self.visited_folders = []
        self.recursion_count = 0
        self.start_text()
        # self.monitor_directory(argv[3])

    def monitor_directory(self, seconds):
        if seconds == 0:
            print("Syncing directories: once")
            return self.start_scan()
        else:
            loop_length = seconds
            print("Syncing directories: every %s seconds." % loop_length)
        while True:
            try:
                self.start_scan()
                time.sleep(loop_length)
            except KeyboardInterrupt:
                self.exit_scan()

    def start_text(self):
        print("\nStarting directory monitor/scan at: %s\n" % self.start_time)

    def start_scan(self):
        # print("start_scan(%s)" % self)
        while self.source_directory_has_contents():
            source_folder_children = self.get_folders_in_directory(self.source_dir)
            source_folder_children_count = len(source_folder_children)
            self.move_files_in_root(self.source_dir)
            self.visited_folders.append(self.source_dir)
            self.recursive_scan(source_folder_children)
        print("Source directory is empty.")
        self.exit_scan()

    def recursive_scan(self, path_list):
        self.recursion_count += 1
        #print("recursive_scan(%s)" % path_list)
        for active_folder in path_list:
            if not self.source_directory_has_contents():
                self.exit_scan()
            if active_folder == self.source_dir:
                #print("Parent found... exiting.")
                self.start_scan()
            parent_folder = os.path.dirname(active_folder)
            parent_folder_children = self.get_folders_in_directory(parent_folder)
            active_folder_children = self.get_folders_in_directory(active_folder)
            active_folder_children_count = len(active_folder_children)
            #print("-----------------------------")
            #print("ACTIVEFOLDER = %s" % active_folder)
            active_folder = os.path.abspath(active_folder)
            self.move_files_in_root(active_folder)
            if active_folder not in self.visited_folders:
                print()
                print("FOUND: NEW FOLDER: %s " % os.path.basename(active_folder))
                self.visited_folders.append(active_folder)
                self.copy_folder(active_folder, self.destination_dir)
            if active_folder in self.visited_folders:
                if len([item for item in active_folder_children if item in self.visited_folders]) == active_folder_children_count:
                    #print("Children match visited folders, visiting parent of active directory.")
                    new_active = str(active_folder)
                    parent_folder = os.path.dirname(new_active)
                    self.remove_folder(active_folder)
                    #self.recursive_scan(parent_folder)
                if len([folder for folder in parent_folder_children if folder in self.visited_folders]) > 0:
                    #print("Unvisited siblings detected.")
                    #print([folder for folder in parent_folder_children if folder not in self.visited_folders])
                    self.recursive_scan(
                        [folder for folder in parent_folder_children if folder not in self.visited_folders])
                if active_folder_children_count == 0:
                    #print("%s has no children, end of tree." % active_folder)
                    self.recursive_scan([parent_folder])
                else:
                    #print("ELSE entered.")
                    self.recursive_scan(active_folder_children)

    @staticmethod
    def get_files_in_directory(path):
        # print("get_files_in_directory(%s)" % path)
        return [os.path.join(path, object) for object in os.listdir(path) if os.path.isfile(os.path.join(path, object)) == True]

    @staticmethod
    def get_folders_in_directory(path):
        return [os.path.join(path, object) for object in os.listdir(path) if
                os.path.isdir(os.path.join(path, object)) == True]

    def exit_scan(self):
        print("\nTimes recurred: %s" % self.recursion_count)
        print("Exiting program.\n")
        print("--- %s seconds ---" % (time.time() - self.start_time_seconds))
        exit()

    def move_files_in_root(self, path):
        for item in self.get_files_in_directory(path):
            if item not in self.visited_files:
                if self.file_is_changed_within_5_seconds(item):
                    pass
                self.move_file(item, self.destination_dir)
                self.visited_files.append(item)

    @staticmethod
    def file_is_changed_within_5_seconds(source_file):
        last_accessed = os.path.getatime(source_file)
        print()
        print("FOUND: %s" % os.path.basename(source_file))
        print("Waiting 5 seconds.")
        for scan_period in range(0, 4):
            if last_accessed != os.path.getatime(source_file):
                print("%s has changed" % source_file)
                return True
            time.sleep(1)
        return False

    def move_file(self, source, destination):
        try:
            destination_folder = os.path.join(destination,
                                              os.path.dirname(os.path.relpath(source, self.source_dir)))
            # print("rel: %s" % os.path.dirname(os.path.relpath(source, self.source_dir)))
            # print("destination_folder: %s" % destination_folder)
            # print("%s, %s" % (os.path.exists(destination) == True, destination_folder))
            try:
                # print("makedirs: %s" % destination_folder)
                os.makedirs(os.path.abspath(destination_folder))
            except FileExistsError:
                # print("makedirs FAILED.")
                pass
            shutil.move(source, destination_folder)
        except shutil.Error:  # Need to catch "same_file errors"
            pass

    def copy_folder(self, source, destination):
        destination_folder = os.path.join(destination,
                                      os.path.relpath(source, self.source_dir))
        # print("copy_folder(%s, %s)" % (source, destination_folder))
        try:
            os.makedirs(os.path.abspath(destination_folder))
        except FileExistsError:
            pass

    def remove_folder(self, source):
        if source == self.source_dir:
            print("Program tried to delete source directory, yo.")
            exit()
        try:
            shutil.rmtree(source)
        except OSError:
            print("Folder contains files. Rmdir FAILED.")
            pass

    def source_directory_has_contents(self):
        path = self.source_dir
        count_of_directory_children = len([os.path.join(path, object) for object in os.listdir(path)])
        if count_of_directory_children > 0:
            return True
        return False
