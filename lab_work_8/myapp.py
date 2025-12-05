from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")
main_author = Author.Author("Vadim", "P4150")


result = template.render(
  myapp="CurrenciesListApp",
  navigation=[{'caption': 'Основная страница',
               'href': "https://nickzhukov.ru" 
              },],
  author_name=main_author.name,
  author_group=main_author.group,
  )



if __name__ == '__main__':
    print(result)