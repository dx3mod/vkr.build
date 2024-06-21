# vkr.css

Готовая CSS-тема для вёрстки курсовых/дипломных работ с помощью [WeasyPrint](https://weasyprint.org/) или другого решения.

<!-- ### Мотивация

Использование *традиционного* Microsoft Word-а  или другого [WYSIWYG-редактора][WYSIWYG] требует ручного оформления элементов, 
что не всегда поддаётся простой автоматизации, для которой требуется специальные знания.

Поэтому альтернативным решением этой проблемы выступают автоматизированные системы вёрстки, вроде TeX. Но и с ними не всё так просто  -->

### Фичи

- [x] Автоматическая нумерация (страниц, рисунков, таблиц)
- [x] Заголовки (h1, h2, h3)
- [x] Приложения
- [x] Блоки кода
- [x] Сноски
- [X] Изображения
- [X] Таблицы
- [X] Списки
- [ ] Оглавление


## Использование

1. Получить HTML-страничку из Markdown (опционально)
    ```console
    pandoc kyrsach.md -o kyrsach.html --css vkr.css --standalone
    ```
2. Преобразовать в PDF с помощью WeasyPrint или другого инструмента
    ```console
    weasyprint kyrsach.html kyrsach.pdf
    ```

#### Переменные

```css
:root {
  --start-page: 3;

  --chapter: "Глава ";
  /* Расположение подзаголовков. */
  --subheader-align: center;

  /* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type */
  --chapter-number-style: upper-roman;

  /* Шрифт кода. */
  --font-mono: monospace;
}
```


[WYSIWYG]: https://ru.wikipedia.org/wiki/WYSIWYG