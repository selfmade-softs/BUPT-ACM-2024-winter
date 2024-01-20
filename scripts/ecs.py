class all_elements_contains_name(object):
    def __init__(self, locator, name):
        self.locator = locator
        self.name = name

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        for element in elements:
            if self.name not in element.text:
                return False
        return elements