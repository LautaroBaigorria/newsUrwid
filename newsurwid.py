#!/usr/bin/python
import urwid
import news2
from tqdm import tqdm
from bs4 import BeautifulSoup


# choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()
# lista = ['http://rss.slashdot.org/Slashdot/slashdot','http://www.digg.com/rss/index.xml','https://www.tecmint.com/feed/','https://www.reddit.com/r/Python/.rss']
news = news2.News()

# feedObject = news.parselink(lista[0]["link"])
def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def menu():
    lista = news.loadyaml()
    title = "News"
    body = [urwid.Text(title), urwid.Divider()]
    for element in tqdm(lista):
        button = urwid.Button(element["titulo"])
        # linea a conectar con submenu()
        # urwid.connect_signal(button, 'click', item_chosen, c["link"])
        singleLink = element["link"]
        urwid.connect_signal(button, 'click',submenu,singleLink)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def submenu(button, singleLink):
    feedObject = news.parselink(singleLink)
    text = f"{feedObject.feed.title}\n "
    body = [urwid.Text(text)]
    for element in feedObject.entries:
        textElement = urwid.Button(f"{element.title}\n")
        body.append(textElement)
        urwid.connect_signal(textElement,'click',showArticle,element)
    # response = urwid.Text(text)
    testing = urwid.Button('Probar')
    body.append(testing)
    done = urwid.Button(u'Salir')
    body.append(done)
    urwid.connect_signal(done, 'click', exit_program)
    urwid.connect_signal(testing, 'click', showArticle, feedObject.entries[0])
    main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
def showArticle(button, feedElement):
    '''funciona'''
    body = []
    text = f"{feedElement.title} \n {feedElement.link} \n {feedElement.description}"
    if (bool(BeautifulSoup(text, "html.parser").find())):
        soup = BeautifulSoup(text,features="lxml")
        text = soup.get_text()
    response = urwid.Text([text])
    done = urwid.Button(u'Salir')
    menuButton = urwid.Button('Volver')
    body.append(response)
    body.append(done)
    body.append(menuButton)
    urwid.connect_signal(done, 'click', exit_program)
    # urwid.connect_signal(menuButton, 'click', submenu, feedElement.feed.link)
    main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
    # main.original_widget = urwid.Filler(urwid.Pile([response,urwid.AttrMap(done, None, focus_map='reversed'),urwid.AttrMap(menuButton, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()

if __name__ == '__main__':
    main = urwid.Padding(menu(), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill('\N{MEDIUM SHADE}') , align='center', width=('relative', 60),valign='middle', height=('relative', 60), min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')], unhandled_input=exit_on_q).run()