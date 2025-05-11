from os import path, listdir


class FileCollectorServices:
    def __init__(self, base_dir: str, file_format: str) -> None:
        self._base_dir = base_dir
        self._file_format = file_format


    def collect(self, input_elements: list[str]) -> list[str]:
        file_paths = []
        for element in input_elements:
            if element.lower().endswith(self._file_format):
                if path.isabs(element) and path.isfile(element):
                    file_paths.append(path.abspath(element))
                else:
                    created_path = path.join(self._base_dir, element)
                    if path.isfile(created_path):
                        file_paths.append(path.abspath(created_path))
                    else:
                        raise FileNotFoundError(f'Некорректно передан путь к файлу/директории "{element}"')
            else:
                directory_path = element if path.isabs(element) else path.join(self._base_dir, element)
                if path.isdir(directory_path):
                    for element in listdir(directory_path):
                        if element.lower().endswith(self._file_format):
                            created_path = path.join(directory_path, element)
                            if path.isfile(created_path):
                                file_paths.append(path.abspath(created_path))
                else:
                    raise FileNotFoundError(f'Некорректно передан путь к файлу/директории "{element}"')

        return file_paths
