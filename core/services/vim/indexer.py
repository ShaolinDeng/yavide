import logging
from common.yavide_utils import YavideUtils

class VimIndexer(object):
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance
        self.op = {
            0x0 : self.__run_on_single_file,
            0x1 : self.__run_on_directory,
            0x2 : self.__drop_single_file,
            0x3 : self.__drop_all,
            0x10 : self.__go_to_definition,
            0x11 : self.__find_all_references
        }

    def __call__(self, op_id, args):
        self.op.get(op_id, self.__unknown_op)(args)

    def __unknown_op(self, args):
        logging.error("Unknown operation triggered! Valid operations are: {0}".format(self.op))

    def __run_on_single_file(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_RunOnSingleFileCompleted()")

    def __run_on_directory(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_RunOnDirectoryCompleted()")

    def __drop_single_file(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_DropSingleFileCompleted()")

    def __drop_all(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_DropAllCompleted()")

    def __go_to_definition(self, location):
        if location:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_GoToDefinitionCompleted('" + location.file.name + "', " + str(location.line) + ", " + str(location.column) + ", " + str(location.offset) + ")")
        else:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_GoToDefinitionCompleted('', 0, 0, 0")

    def __find_all_references(self, references):
        quickfix_list = []
        for location in references:
            quickfix_list.append(
                "{'filename': '" + str(location[0]) + "', " +
                "'lnum': '" + str(location[2]) + "', " +
                "'col': '" + str(location[3]) + "', " +
                "'type': 'I', " +
                "'text': '" + str(location[0]) + "'}" # TODO Put something more meaningful here, i.e. the corresponding source code line
            )

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_FindAllReferencesCompleted(" + str(quickfix_list).replace('"', r"") + ")")
        logging.debug("References: " + str(quickfix_list))
