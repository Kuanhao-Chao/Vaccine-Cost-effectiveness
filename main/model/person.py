import uuid
import random
from .parameters import CurrStatus, RouteStatus, AgeGroup, ContactRate, VaccineRate, InfectionRate, SeekTreatmentRate, MedicineIntakeRate, SevereRate, FatalityRate, effectiveness, AliveDeath
# from .parameters import IDX_SEEK_TREATMENT_PROB

class Person():
    def __init__(self, age, initial_idx_case=False):
        self.id = str(uuid.uuid1())
        self.curr_status = CurrStatus.IN_MODEL
        self.day = 0
        self.age = age
        self.age_group = self.set_age_group()
        self.route_status = RouteStatus.TRANSMISSION

        self.youth_contact_rate = self.set_contact_rate('youth')
        self.adult_contact_rate = self.set_contact_rate('adult')
        self.elder_contact_rate = self.set_contact_rate('elder')

        self.vaccine_rate = self.set_vaccine_rate()
        self.vaccine_status = self.set_vaccine_status()

        self.infection_rate = self.set_infection_rate()
        self.infection_status = self.set_infection_status(initial_idx_case)

        self.seek_treatment_rate = self.set_seek_treatment_rate()

        self.seek_treatment_status = False

        self.medicine_intake_rate = self.set_medicine_intake_rate()
        self.medicine_intake_status = False

        self.severe_rate = self.set_severe_rate()
        self.severe_status = False

        self.fatality_rate = self.set_fatality_rate()
        self.effectiveness_mild = effectiveness.MILD
        self.effectiveness_severe = effectiveness.SEVERE
        self.effectiveness_death = effectiveness.DEATH

    ## static
    def set_seek_treatment_rate(self):
        if self.age <= 18:
            return SeekTreatmentRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return SeekTreatmentRate.ADULT_RT
        elif self.age >= 65:
            return SeekTreatmentRate.ELDER_RT

    ## static
    def set_seek_treatment_status(self):
        if self.infection_status is False:
            return False
        rand_dice = random.random() < self.seek_treatment_rate.value
        if rand_dice:
            return True
        else:
            return False


    ##########################
    ## Outside Calling func ##
    ##########################
    def choose_route(self):
        if self.route_status is RouteStatus.TRANSMISSION:
            self.seek_treatment_status = self.set_seek_treatment_status()
            if self.seek_treatment_status is True:
                self.route_status = RouteStatus.SEEKTREATMENT
                self.medicine_intake_status = self.set_medicine_intake_status()
                self.severe_status = self.set_severe_status()
            elif self.seek_treatment_status is False:
                pass
        elif self.route_status is RouteStatus.SEEKTREATMENT:
            pass

    ## static
    def set_age_group(self):
        if self.age <= 18:
            return AgeGroup.YOUTH_GRP
        elif self.age > 18 and self.age <65:
            return AgeGroup.ADULT_GRP
        elif self.age >= 65:
            return AgeGroup.ELDER_GRP

    ## static
    def set_contact_rate(self, category):
        if self.age <= 18:
            if category is 'youth':
                return ContactRate.SAME_GRP
            elif category is 'adult':
                return ContactRate.DIFF_GRP
            elif category is 'elder':
                return ContactRate.DIFF_GRP
        elif self.age > 18 and self.age <65:
            if category is 'youth':
                return ContactRate.DIFF_GRP
            elif category is 'adult':
                return ContactRate.SAME_GRP
            elif category is 'elder':
                return ContactRate.DIFF_GRP
        elif self.age >= 65:
            if category is 'youth':
                return ContactRate.DIFF_GRP
            elif category is 'adult':
                return ContactRate.DIFF_GRP
            elif category is 'elder':
                return ContactRate.SAME_GRP

    ## static
    def set_vaccine_rate(self):
        if self.age <= 18:
            return VaccineRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return VaccineRate.ADULT_RT
        elif self.age >= 65:
            return VaccineRate.ELDER_RT

    ## The status of this function is dynamic
    def set_vaccine_status(self):
        if self.route_status is RouteStatus.TRANSMISSION:
            rand_dice = random.random() < self.vaccine_rate.value
            if rand_dice:
                return True
            else:
                return False

    ## dynamic
    def set_infection_rate(self):
        if self.vaccine_status is True:
            if self.age <= 18:
                return InfectionRate.YOUTH_V_RT
            elif self.age > 18 and self.age <65:
                return InfectionRate.ADULT_V_RT
            elif self.age >= 65:
                return InfectionRate.ELDER_V_RT
        elif self.vaccine_status is False:
            if self.age <= 18:
                return InfectionRate.YOUTH_NV_RT
            elif self.age > 18 and self.age <65:
                return InfectionRate.ADULT_NV_RT
            elif self.age >= 65:
                return InfectionRate.ELDER_NV_RT

    def set_infection_status(self, initial_idx_case):
        if initial_idx_case is True:
            return True
        rand_dice = random.random() < self.infection_rate.value
        if rand_dice:
            return True
        else:
            return False

    ## static
    def set_medicine_intake_rate(self):
        if self.age <= 18:
            return MedicineIntakeRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return MedicineIntakeRate.ADULT_RT
        elif self.age >= 65:
            return MedicineIntakeRate.ELDER_RT

    def set_medicine_intake_status(self):
        if self.seek_treatment_status is True:
            rand_dice = random.random() < self.medicine_intake_rate.value
            if rand_dice:
                return True
            else:
                return False
        else:
            return False

    def set_severe_rate(self):
        if self.medicine_intake_status is True:
            if self.age <= 18:
                return SevereRate.YOUTH_48_RT
            elif self.age > 18 and self.age <65:
                return SevereRate.ADULT_48_RT
            elif self.age >= 65:
                return SevereRate.ELDER_48_RT
        elif self.medicine_intake_status is False:
            if self.age <= 18:
                return SevereRate.YOUTH_N48_RT
            elif self.age > 18 and self.age <65:
                return SevereRate.ADULT_N48_RT
            elif self.age >= 65:
                return SevereRate.ELDER_N48_RT

    def set_severe_status(self):
        if self.seek_treatment_status is True:
            rand_dice = random.random() < self.severe_rate.value
            if rand_dice:
                return True
            else:
                self.recovery()
                return False
        else:
            return False

    def set_fatality_rate(self):
        if self.age <= 18:
            return FatalityRate.YOUTH_RT
        elif self.age > 18 and self.age <65:
            return FatalityRate.ADULT_RT
        elif self.age >= 65:
            return FatalityRate.ELDER_RT

    def in_model(self):
        self.curr_status = CurrStatus.IN_MODEL

    def recovery(self):
        self.curr_status = CurrStatus.RECOVERY

    def death(self):
        self.curr_status = CurrStatus.DEATH

    def cycle_reached(self):
        self.curr_status = CurrStatus.CYCLE_REACHED

    def set_current_status(self):
        if self.route_status is RouteStatus.TRANSMISSION:
            if self.day > 7:
                self.cycle_reached()
            else:
                self.in_model()
        elif self.route_status is RouteStatus.SEEKTREATMENT:
            if self.severe_status:
                rand_dice = random.random() < self.fatality_rate.value
                if rand_dice:
                    self.death()
                else:
                    self.recovery()
            else:
                self.recovery()

    ##########################
    ## Outside Calling func ##
    ##########################
    def day_passed(self):
        self.day += 1
        self.set_current_status()
        # if self.day > 7:
        #     self.cycle_reached()
        # if self.curr_status is not CurrStatus.DEATH:
        #     self.recovery()


# def HealthPerson(Person):
#     def __init__(self, age, vaccine_rate, affected_rate):
#         Person(age, vaccine_rate, infection_rate)
#
# def IdxCasePerson(Person):
#     def __init__(self, age, vaccine_rate, affected_rate, hosp_status, sever_rate, mortality_rate, symptom):
#         Person(age, vaccine_rate, infection_rate)
#         self.hosp_status = hosp_status
#         self.sever_rate = sever_rate
#         self.mortality_rate = mortality_rate
#         self.symptom = symptom
