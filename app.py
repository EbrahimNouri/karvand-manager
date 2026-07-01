import json
import os

bootcamp_path = "./data/karvands.json"
report_path = "./data/report.json"
bootcamp_title = "AI BOOTCAMP 145"
bootcamp_year = 2026


class Report:
    def __init__(self, karvands: list):
        all_of_skills = []
        for karvand in karvands:
            all_of_skills.extend(karvand.skills)
        self.total_karvands = len(karvands)
        self.total_skills = len(all_of_skills)

        if all_of_skills:
            self.average_skills = sum(skill.score for skill in all_of_skills) / len(all_of_skills)
        else:
            self.average_skills = 0

        self.cities = set()
        for karvand in karvands:
            if karvand.city and karvand.city.strip():
                self.cities.add(karvand.city.strip().lower())

        self.unique_skills = set()
        for skill in all_of_skills:
            if skill.name and skill.name.strip():
                self.unique_skills.add(skill.name.strip().lower())

    def __str__(self):
        return f"total_karvands: {self.total_karvands}\ntotal_skills: {self.total_skills}\naverage_skills: {self.average_skills:.2f}\ncities: {', '.join(self.cities) if self.cities else 'none'}\nunique_skills: {', '.join(self.unique_skills) if self.unique_skills else 'none'}"

    def to_json(self):
        return {
            "total_karvands": self.total_karvands,
            "total_skills": self.total_skills,
            "average_skills": self.average_skills,
            "cities": list(self.cities),
            "unique_skills": list(self.unique_skills)
        }


class Education:
    def __init__(self, degree: str, field: str):
        self.degree = degree
        self.field = field

    def __str__(self):
        return f"degree: {self.degree}\nfield: {self.field}"

    def to_json(self):
        return {
            "degree": self.degree,
            "field": self.field
        }

    @staticmethod
    def from_json(data):
        return Education(data["degree"], data["field"])


class Skill:
    def __init__(self, name: str, level: str, score: int):
        self.name = name
        self.level = level
        self.score = score

    def __str__(self):
        return f"name: {self.name}\nlevel: {self.level}\nscore: {self.score}"

    def to_json(self):
        return {
            "name": self.name,
            "level": self.level,
            "score": self.score
        }

    @staticmethod
    def from_json(data):
        return Skill(data["name"], data["level"], data["score"])


class Karvand:
    def __init__(self, karvand_id: int, name: str, email: str, city: str, education: Education, skills: list[Skill]):
        self.karvand_id = karvand_id
        self.name = name
        self.email = email
        self.city = city
        self.education = education
        self.skills = skills

    def __str__(self):
        skills_str = "\n".join([str(skill) for skill in self.skills])
        return f"id: {self.karvand_id}\nname: {self.name}\nemail: {self.email}\ncity: {self.city}\neducation:\n{self.education}\nskills:\n{skills_str}"

    def to_json(self):
        return {
            "id": self.karvand_id,
            "name": self.name,
            "email": self.email,
            "city": self.city,
            "education": self.education.to_json(),
            "skills": [skill.to_json() for skill in self.skills]
        }

    @staticmethod
    def from_json(data):
        education_obj = Education.from_json(data["education"])
        skills_objs = [Skill.from_json(skill) for skill in data["skills"]]
        return Karvand(
            data["id"],
            data["name"],
            data["email"],
            data["city"],
            education_obj,
            skills_objs
        )

    def update(self, name: str = None, email: str = None, city: str = None,
               education: Education = None, skills: list[Skill] = None):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if city is not None:
            self.city = city
        if education is not None:
            self.education = education
        if skills is not None:
            self.skills = skills

    def save(self):
        bootcamp = Bootcamp.load()
        bootcamp.karvands.append(self)
        bootcamp.save()


def get_year_input() -> int:
    year = input("Enter bootcamp title: ")
    if not year.isnumeric():
        print("Invalid bootcamp year.")
        return get_year_input()
    year = int(year)
    if year < 2025:
        print("Invalid bootcamp year.")
        return get_year_input()
    return year


class Bootcamp:
    def __init__(self, title: str, year: int, karvands: list[Karvand]):
        self.title = title
        self.year = year
        self.karvands = karvands

    def __str__(self):
        if not self.karvands:
            return f"title: {self.title}\nyear: {self.year}\n\nno karvands found"

        karvands_str = "\n\n".join([str(k) for k in self.karvands])
        return f"title: {self.title}\nyear: {self.year}\n\nkarvands:\n{karvands_str}"

    def to_json(self):
        return {
            "title": self.title,
            "year": self.year,
            "karvands": [karvand.to_json() for karvand in self.karvands]
        }

    @staticmethod
    def from_json(data):
        karvands_objs = [Karvand.from_json(k) for k in data["karvands"]]
        return Bootcamp(data["title"], data["year"], karvands_objs)

    @staticmethod
    def check_files() -> 'Bootcamp':
        os.makedirs(os.path.dirname(bootcamp_path), exist_ok=True)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        file_ok = True
        if not os.path.exists(bootcamp_path):
            file_ok = False
        else:
            try:
                with open(bootcamp_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, dict) or "title" not in data or "karvands" not in data:
                        file_ok = False
                    elif not isinstance(data["karvands"], list):
                        file_ok = False
            except (json.JSONDecodeError, ValueError, KeyError):
                file_ok = False

        if not file_ok:
            if bootcamp_title:
                title = bootcamp_title
            else:
                title = input("Enter bootcamp title: ")
            if bootcamp_year:
                year = bootcamp_year
            else:
                year = get_year_input()
            bootcamp = Bootcamp(title, year, [])
            bootcamp.save()
            return bootcamp

        report_ok = True
        if not os.path.exists(report_path):
            report_ok = False
        else:
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, dict) or "total_karvands" not in data:
                        report_ok = False
            except (json.JSONDecodeError, ValueError, KeyError):
                report_ok = False

        if not report_ok:
            bootcamp = Bootcamp.load_from_file()
            bootcamp.save()
            return bootcamp

        return Bootcamp.load_from_file()

    def add_karvand(self, karvand: Karvand):
        if self.get_karvand_by_id(karvand.karvand_id):
            raise ValueError(f"Karvand with ID {karvand.karvand_id} already exists")

        self.karvands.append(karvand)
        print(f"Karvand {karvand.name} with ID {karvand.karvand_id} added")

    def remove_karvand(self, karvand_id: int):
        for i, karvand in enumerate(self.karvands):
            if karvand.karvand_id == karvand_id:
                removed = self.karvands.pop(i)
                print(f"Karvand {removed.name} with ID {removed.karvand_id} removed")
                return removed
        raise ValueError(f"Karvand with ID {karvand_id} not found")

    def get_karvand_by_id(self, karvand_id: int) -> Karvand | None:
        for karvand in self.karvands:
            if karvand.karvand_id == karvand_id:
                return karvand
        return None

    def get_karvand_by_name(self, name: str) -> Karvand | None:
        for k in self.karvands:
            if k.name == name:
                return k
        return None

    def get_all_karvands(self) -> list[Karvand]:
        return self.karvands

    def update_karvand(self, karvand_id: int, name: str = None, email: str = None,
                       city: str = None, education: Education = None,
                       skills: list[Skill] = None):
        karvand = self.get_karvand_by_id(karvand_id)
        if not karvand:
            raise ValueError(f"Karvand with ID {karvand_id} not found")

        karvand.update(name, email, city, education, skills)
        print(f"Karvand with ID {karvand_id} updated")
        return karvand

    def search_karvands(self, keyword: str) -> list[Karvand]:
        results = []
        keyword_lower = keyword.lower()
        for k in self.karvands:
            if keyword_lower in k.name.lower() or keyword_lower in k.email.lower():
                results.append(k)
        return results

    def count_karvands(self) -> int:
        return len(self.karvands)

    def get_next_id(self) -> int:
        if not self.karvands:
            return 1
        return max(k.karvand_id for k in self.karvands) + 1

    def save(self):
        os.makedirs(os.path.dirname(bootcamp_path), exist_ok=True)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(bootcamp_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_json(), f, ensure_ascii=False, indent=2)

        reported = Report(self.karvands)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(reported.to_json(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_from_file() -> 'Bootcamp':
        with open(bootcamp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Bootcamp.from_json(data)

    @staticmethod
    def load() -> 'Bootcamp':
        return Bootcamp.check_files()


if __name__ == "__main__":
    Bootcamp.check_files()