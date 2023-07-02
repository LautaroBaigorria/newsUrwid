#!/usr/bin/python
import urwid
import news2

class App(object):
    
    def __init__(self) -> None:
        self.news = news2.News()
    
    def exit_on_q(self,key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def menu(self):
        lista = self.news.loadyaml()
        title = "News"
        body = [urwid.Text(title), urwid.Divider()]
        for element in lista:
            button = urwid.Button(element["titulo"])
            # linea a conectar con submenu()
            # urwid.connect_signal(button, 'click', item_chosen, c["link"])
            singleLink = element["link"]
            urwid.connect_signal(button, 'click',self.submenu,singleLink)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        buttonShowRecentNews = urwid.Button("Mostrar noticias recientes")
        urwid.connect_signal(buttonShowRecentNews, 'click',self.gridFlowArticles)
        body.append(buttonShowRecentNews)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def menu2(self, button):
        body = []
        lista = self.news.loadyaml()
        title = "News"
        body = [urwid.Text(title), urwid.Divider()]
        for element in lista:
            button = urwid.Button(element["titulo"])
            singleLink = element["link"]
            urwid.connect_signal(button, 'click',self.submenu,singleLink)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))



    def submenu(self, button, singleLink):
        feedObject = self.news.parselink(singleLink)
        text = f"{feedObject.feed.title}\n "
        body = [urwid.Text(text)]
        for element in feedObject.entries:
            textElement = urwid.Button(f"{element.title}\n")
            body.append(textElement)
            urwid.connect_signal(textElement,'click',self.showArticle,element)
            # urwid.connect_signal(textElement, 'click', self.dialog, element)
        # response = urwid.Text(text)
        testing = urwid.Button('Volver al menu anterior')
        body.append(testing)
        done = urwid.Button(u'Salir')
        body.append(done)
        urwid.connect_signal(done, 'click', self.exit_program)
        urwid.connect_signal(testing, 'click', self.menu2)
        main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        
    def showArticle(self, button, feedElement):
        body = [urwid.Text(feedElement.title)]
        text = f"{feedElement.description}"
        text = self.news.htmlTotext(text)
        response = urwid.Text([text])
        done = urwid.Button(u'Salir')
        menuButton = urwid.Button('Volver al menu anterior')
        body.append(response)
        body.append(done)
        body.append(menuButton)
        urwid.connect_signal(done, 'click', self.exit_program)
        # urwid.connect_signal(menuButton, 'click', self.submenu)
        main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        # main.original_widget = urwid.Filler(urwid.Pile([response,urwid.AttrMap(done, None, focus_map='reversed'),urwid.AttrMap(menuButton, None, focus_map='reversed')]))

    def gridFlowArticles(self, button):
        body = []
        cells = []
        feedList = []
        lista = self.news.loadyaml()
        for element in lista:
            feed = self.news.parselink(element["link"])
            feedList.append(feed)
        for element in feedList:
            # feedElement = self.news.parselink(element["link"])
            if element.entries:
                textToInclude = f"{element['feed']['title']}  -  {element.entries[0].title}"
                cells.append(urwid.Text(textToInclude, align='left'))
            lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            
            
        cell_width = 20
        h_sep = 1
        v_sep = 1
        align = 'center'
        grid = urwid.GridFlow(cells, cell_width, h_sep, v_sep, align)
        body.append(grid)
        main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

        # grid_filler = urwid.Filler(grid, valign='middle')
        # main.original_widget = grid_filler

    def exit_program(self, button):
        raise urwid.ExitMainLoop()
    
    

if __name__ == '__main__':
    app = App()
    main = urwid.Padding(app.menu(), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill('\N{MEDIUM SHADE}') , align='center', width=('relative', 60),valign='middle', height=('relative', 60), min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')], unhandled_input=app.exit_on_q).run()