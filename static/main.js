import { prettyFormatDate } from "./helpers.js"

const table = document.getElementById('articlesTable')

class Article {

    constructor(articleData) {

        this.category = articleData.category
        this.dateObj = new Date(articleData.publishedYear,articleData.publishedMonth,articleData.publishedDay)
        this.prettyDate = prettyFormatDate(articleData.publishedYear,articleData.publishedMonth,articleData.publishedDay)
        this.publishedYear = articleData.publishedYear
        this.url = articleData.url
        this.db_id = articleData.db_id
        this.title = articleData.title
        this.source = articleData.source
        this.irrelevant = articleData.relevant
    }

    constructRow() {
        /// creating elements
        const row = document.createElement('tr')
        const dateCell = document.createElement('td')
        const titleCell = document.createElement('td')
        const controlsCell = document.createElement('td')
        const relevanceButton = document.createElement('button')

        // date cell content
        dateCell.classList.add('dateCell')
        dateCell.innerHTML = this.prettyDate

        controlsCell.classList.add('controlsCell')
        relevanceButton.innerText = '❌'
        relevanceButton.addEventListener('click', () => {
            this.markIrrelevant()
        });
        controlsCell.appendChild(relevanceButton)

        titleCell.innerHTML = `<a href='${this.url}' target="_blank" class='newsTitle'>${this.title}</a><br><i class='newsSourceSmall'>${this.source}</i>`

        if (this.irrelevant) {
            row.classList.add('irrelevantArticle')
        }


        // build table DOM
        row.appendChild(dateCell)
        row.appendChild(titleCell)
        row.appendChild(controlsCell)
        row.style.display === 'block'
        table.appendChild(row)

        this.row = row

    }

    hide() {
        this.row.style.display = 'none'
    }

    show() {
        this.row.style.display = ''
    }

    async markIrrelevant() {
        this.irrelevant = true
        this.row.classList.add('irrelevantArticle')
        const response = await fetch(`/markIrrelevant?articleID=${this.db_id}`);
        this.checkResponse(response)


    }

    checkResponse(response) {
        if (response.status != 200) {
            console.error('Bad response: ', response)
        }
    }

}

class articleManager {

    constructor(rawArticles) {

        this.searchTerm = '';
        const searchInput = document.getElementById('articleSearch');

        searchInput.addEventListener('input', (e) => {
            this.searchTerm = e.target.value.toLowerCase();
            this.updateUI(); // Refresh the list as you type
        });

        this.articles = []
        this.sources = {}
        this.categories = []
        this.displayIrrelevant = false

        // setting up articles from the raw article data.
        // we declare rawArticles in the html file, in global scope, due to flask limitations

        rawArticles.forEach(articleData => {

            const articleObj = new Article(articleData)
            this.articles.push(articleObj)

            const category = articleObj.category || 'Misc';
            const source = articleObj.source


            if (!this.sources[source]) {
                this.sources[source] = {

                    'source': source,
                    'category': category,
                    'display': true

                };
            }
            if (!this.categories.find(c => c === category)) {
                this.categories.push(category)
            }


        })

        this.sortByDate()

        this.articles.forEach(a => {
            a.constructRow()
        })

        this.updateUI()

        document.getElementById('selection').appendChild(this.buildSourceUIList())

    }

    sortByDate() {
        this.articles.sort((a, b) => b.dateObj - a.dateObj);
    }

    updateUI() {
        this.articles.forEach(a => {
            if (a.irrelevant && !this.displayIrrelevant) {
                a.hide()
                return
            }
    // Check Source toggle and Search term
            const matchesSource = this.sources[a.source].display === true;
            const matchesSearch = a.title.toLowerCase().includes(this.searchTerm) ||
                                a.source.toLowerCase().includes(this.searchTerm);

            if (matchesSource && matchesSearch) {
                a.show();
            } else {
                a.hide();
            }
        });
    }

    displaySource(source, display) {
        /// call this like (IH, true) if you would like to show all IH articles. you must then call updateUI() to effectuate it.
        this.sources[source].display = display
    }

    buildSourceUIList() {


        const div = document.createElement('div')
        div.innerHTML = `<input type='checkbox' id='displayIrrelevantBox' />
                         <label for='displayIrrelevantBox'>Display articles marked irrelevant?</label>   `

        div.querySelector('#displayIrrelevantBox').addEventListener('click', () => {
            if (this.displayIrrelevant) {this.displayIrrelevant = false}
            else {this.displayIrrelevant = true}
            this.updateUI()
        })




        this.categories.forEach(c => {

            const title = document.createElement('h3')
            const sourcesInCat = Object.values(this.sources).filter(s => s.category === c);

            title.innerText = c
            title.addEventListener('click', () => {
                // is ANY source in this category currently displayed?
                const isAnyVisible = sourcesInCat.some(s => s.display === true);

                // toggle: If any are visible, hide all. If all are hidden, show all.
                sourcesInCat.forEach(source => {
                    source.display = !isAnyVisible;
                });

                if (isAnyVisible) {
                    div.querySelectorAll('button').forEach(b => {
                        if (b.dataset.category === c) {b.classList.add('hidden')}
                    })
                    title.classList.add('hidden')

                } else {

                    div.querySelectorAll('button').forEach(b => {
                        if (b.dataset.category === c) {b.classList.remove('hidden')}
                    })

                    title.classList.remove('hidden')
                }

                this.updateUI();
            });
            div.appendChild(title)

            sourcesInCat.forEach(s => {
                const button = document.createElement('button')
                button.innerText = s.source
                console.log(this.sources, s.source)
                button.addEventListener('click', () => {
                    if (this.sources[s.source].display === true) {
                        this.sources[s.source].display = false
                        button.classList.add('hidden')
                    } else {
                        this.sources[s.source].display = true
                        button.classList.remove('hidden')
                    }
                    console.log(this.sources[s.source].display)
                    this.updateUI()
                })
                button.dataset.category = this.sources[s.source].category
                div.appendChild(button)
            })
        })

        return div
    }
    

}

const articleMan = new articleManager(rawArticles)

