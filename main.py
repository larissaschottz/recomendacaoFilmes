import imdb
import pandas as pd
import PySimpleGUI as sg


def obter_filmes_por_ano(ano):
    ia = imdb.IMDb()
    movies = ia.search_movie(str(ano))
    return movies


def obter_ano_lancamento(filme):
    try:
        return filme['year']
    except KeyError:
        return None


def criar_janela(layout):
    return sg.Window('Recomendação de Filmes', layout, resizable=True, finalize=True)


def main():
    layout = [
        [sg.Text('Digite o ano de lançamento:'), sg.Input(key='-ANO-', size=(10, 1)), sg.Button('Buscar')],
        [sg.Text('Filmes Recomendados:')],
        [sg.Listbox(values=[], key='-FILMES-', size=(50, 10))],
        [sg.Button('Sair')]
    ]

    janela = criar_janela(layout)

    while True:
        event, values = janela.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break
        elif event == 'Buscar':
            ano = values['-ANO-']
            try:
                ano = int(ano)
                filmes = obter_filmes_por_ano(ano)
                filmes_data = [{'Título': filme['title'], 'Ano': obter_ano_lancamento(filme)} for filme in filmes if
                               obter_ano_lancamento(filme) == ano]
                df_filmes = pd.DataFrame(filmes_data)

                if not df_filmes.empty:
                    janela['-FILMES-'].update(values=df_filmes['Título'].tolist())
                else:
                    sg.popup('Nenhum filme foi lançado neste ano. Por favor, digite outro ano.')

            except ValueError:
                sg.popup_error('Por favor, insira um ano válido.')

    janela.close()


if __name__ == '__main__':
    main()

