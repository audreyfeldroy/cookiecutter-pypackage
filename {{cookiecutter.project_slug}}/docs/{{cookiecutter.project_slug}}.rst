{{cookiecutter.project_slug}}
{% for _ in cookiecutter.project_slug %}={% endfor %}

.. toctree::
   :maxdepth: 3
   :hidden:

   readme
   api_reference
   contributing
   history


{{ cookiecutter.project_short_description }}

.. grid:: 1 2 2 2
    :gutter: 4

    .. grid-item-card::
        :link: readme.html
        :text-align: center
        :padding: 0 0 3 3

        **Getting Started**
        ^^^^

        .. raw:: html

            <i class="fa-solid fa-rocket icon-style"></i>


    .. grid-item-card::
        :link: api_reference
        :link-type: ref
        :text-align: center
        :padding: 0 0 3 3

        **API Reference**
        ^^^^

        .. raw:: html

            <i class="fa-solid fa-file-lines icon-style"></i>


    .. grid-item-card::
        :link: contributing.html
        :text-align: center
        :padding: 0 0 3 3

        **Contributing**
        ^^^^

        .. raw:: html

            <i class="fa-solid fa-pen icon-style"></i>

    .. grid-item-card::
        :link: history.html
        :text-align: center
        :padding: 0 0 3 3

        **History**
        ^^^^

        .. raw:: html

            <i class="fa-solid fa-clock-rotate-left icon-style">
            </i>
