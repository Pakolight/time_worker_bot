from db_worck import args_all
from loguru import logger


class Table_data:
    arg = iter(args_all)
    time_arg = None
    add_arg = []

    def update(self):
        try:
            self.time_arg = next(self.arg)
            logger.debug("True")
            return True

        except StopIteration:
            logger.debug("False")
            return False

    def date(self):
        return str(self.time_arg[0])

    def project(self):
        return str(self.time_arg[1])

    def tasks(self):
        return str(self.time_arg[2])

    def time_start(self):
        return str(self.time_arg[3])

    def time_end(self):
        return str(self.time_arg[4])

    def duration(self):
        return str(self.time_arg[5])

    def d_ex(self):
        return str(self.time_arg[6])

    def km(self):
        return str(self.time_arg[7])

    def km_cost(self):
        return str(self.time_arg[8])

    def o_ex(self):
        return str(self.time_arg[9])

    def ex(self):
        return str(self.time_arg[10])

    def price(self):
        return round(float(self.time_arg[11]),1)

    def creat_list(self):
        if self.update():
            self.add_arg += [self.date(),
                             self.date(),
                             self.tasks(),
                             self.time_start(),
                             self.time_end(),
                             self.duration(),
                             self.d_ex(),
                             self.km(),
                             self.km_cost(),
                             self.o_ex(),
                             self.ex(),
                             self.price(),
                             ]
            self.creat_list()

        else:
            logger.info(f"Done {self.add_arg}")
            return self.add_arg


