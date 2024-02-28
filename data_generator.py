"""
My sources for this script

https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
"""

import random
from faker import Faker
from typing import Any
from sys import argv, exit
from tqdm import tqdm


def generate_dummy_data_profiles(number_of_users: int = 1) -> list[dict[str, Any]]:
  """Generates a given number of profiles using faker package

    Parameters
    ----------
    number_of_users : int, optional
      an integer representing the number of profiles to be generated.

    Returns
    -------
    list[dict[str, Any]]
      a list of generated profiles (key:value pairs).
    """
  fake = Faker(['pt_BR'])
  Faker.seed(random.randint(0, number_of_users * 10))

  generated_data: list[dict[str, Any]] = []

  for _ in tqdm(range(number_of_users), '😎 Generating fake data'):
    profile = fake.profile(fields=['name', 'birthdate', 'mail'])
    generated_data.append({
      'name': profile['name'],
      'date_of_birth': profile['birthdate'],
      'email': profile['mail'],
      'quantity_of_children': random.randint(0, 5),
      'cellphone': '0' + str(random.randint(55555555555, 99999999999))
    })
  
  return generated_data

def write_generated_data_to_txt_file(data: list[dict[str, Any]]) -> None:
  """Writes the generated data to an output TXT file.

    Parameters
    ----------
    data : list[dict[str, Any]]
      a list of generated data.

    Returns
    -------
    None
    """
  with open('user_inserts_sql.txt', 'a', encoding='utf-8') as f1, \
       open('phonenumber_inserts_sql.txt', 'a', encoding='utf-8') as f2:
    f1.write(f"INSERT INTO Users VALUES\n")
    f2.write(f'INSERT INTO Phone_numbers VALUES\n')
    for i, line in tqdm(enumerate(data), '✨ Creating and writing new inserts to a file'):
      last_char = ';' if i == len(data) - 1 else ','
      f1.write(
        f"\t(DEFAULT, '{line['name']}', '{line['date_of_birth']}', '{line['email']}', {line['quantity_of_children']}){last_char}\n"
      )
      f2.write(f"\t(DEFAULT, '{line['cellphone']}', {i+1}){last_char}\n")
    f1.write('\n')
    f2.write('\n')

if __name__ == '__main__':
  try:
    ITERATIONS = int(argv[1])
  except ValueError as ve:
    print('❌ Error - number of iterations must be an integer.')
    exit(1)
  except Exception as e:
    print('❌ Error - an unknow exception was thrown.')
    exit(1)
  write_generated_data_to_txt_file(generate_dummy_data_profiles(ITERATIONS))
