import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl


def plot_counts(df, year):
    cols = df.keys().tolist()
    figs = {}
    for col in cols:
        figs.update(plot_count(df, col, year))

    return figs


def plot_count(df, col, year):
    """
    Core function to plot counts.

    If you want to change the count plots in the report, you would probably
    need to change this function.

    :param df: dataframe
    :param col: column
    :param year: year string
    :return: saved figure object
    """
    # ref: https://www.one-tab.com/page/DHKTSk5CQ1eRobxOZxWnjQ
    # to support CJK fonts
    sns.set(font_scale=2)
    new_fonts = ['AR PL UKai TW'] + mpl.rcParams['font.sans-serif']
    mpl.rcParams['font.sans-serif'] = new_fonts

    col_title = str(col)
    if col_title == 'Title_Categories':
        plot_x_description = 'Job Titles'
    else:
        plot_x_description = col_title

    # plot seaborn countplot on this fig
    fig, ax = plt.subplots(figsize=(12, 8))

    order = get_order(df, col)

    # let seaborn controls ax
    ax = sns.countplot(x=col_title, data=df, order=order)

    ax.set_title(plot_x_description + ' of the Attendees in ' + str(year))
    ax.set_xlabel(plot_x_description)
    ax.set_ylabel('Attendee Number')
    ax.set_xticklabels(order,
                      rotation=90,
                      fontdict={"fontsize": '16'})

    # Tweak spacing to prevent clipping of ylabel or xlabel
    fig.tight_layout()

    return save_fig(col_title)


def save_fig(identifier):
    fig_name = identifier + '.jpg'
    fig_path = '/tmp/' + fig_name
    plt.savefig(fig_path)

    return {identifier: fig_path}


def reorder(order, tag, reverse=False):
    """
    Relocate the tag column to be the last bin of the order.

    :param order: iterable order.
    :param tag: string
    :param reverse: True to put it at the beginning, false to be the last
    :return: ordered order
    """
    order = list(order)
    others_index = order.index(tag)
    order.pop(others_index)
    if reverse:
        order = [tag] + order
    else:
        order.append(tag)

    return order


def get_reorder_by(df, col, pattern, order=None, reverse=False):
    col_counts = df[col].value_counts()

    if order is None:
        order = col_counts.index

    for col_title in col_counts.keys():
        if re.search(pattern, col_title) is not None:
            order = reorder(order, col_title, reverse)

    return order


def get_order(df, col):
    """
    If there is 'others' or 'no record' col, it should be the last bar

    If there are others-like and no-record-like in the meantime, no-record-like
    will be the last one.

    :param df: dataframe
    :param col: col
    :return: iterable
    """
    col_counts = df[col].value_counts()
    order = col_counts.index

    pattern = "Other|other"
    order = get_reorder_by(df, col, pattern, order)

    pattern = "No Record"
    order = get_reorder_by(df, col, pattern, order)

    return order
