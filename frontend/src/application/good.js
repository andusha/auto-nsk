import '../styles/good.scss';
import * as _ from 'lodash';

function priceSlider() {
    const tableFilter = new TableUI(slider)
    const rangeInput = document.querySelectorAll(".range-input input"),
    priceInput = document.querySelectorAll(".price-input input"),
    range = document.querySelector(".slider .progress");
    let priceGap = 1;
    priceInput.forEach((input) => {
    input.addEventListener("input", (e) => {
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);
        updateState(minPrice, maxPrice)

        if (maxPrice - minPrice >= priceGap && maxPrice <= rangeInput[1].max) {
            if (e.target.className === "input-min") {
                rangeInput[0].value = minPrice;
            } else {
                rangeInput[1].value = maxPrice;
            }
        }
    });
    });

    rangeInput.forEach((input) => {
    input.addEventListener("input", (e) => {
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);
        updateState(minVal, maxVal)
        if (maxVal - minVal < priceGap) {
        if (e.target.className === "range-min") {
            rangeInput[0].value = maxVal - priceGap;
        } else {
            rangeInput[1].value = minVal + priceGap;
        }
        } else {
        priceInput[0].value = minVal;
        priceInput[1].value = maxVal;
        }
    });
    });
};

class Filter {
    sortedList;

    constructor(dataList) {
        this.dataList = dataList
    }
    
    orderBy(order, sortMethod) {
        const orderByDict = {'info': 0, 'price': 1, 'amount': 2, 'period': 3}
        this.sortedList = _.orderBy(this.dataList, (p) => p[orderByDict[order]], sortMethod)

        return this.sortedList
    }

}

class TableUI{
    sortedList;

    constructor(elem){
        elem.onclick = this.updateTable.bind(this);
        slider.onchange = this.updateTable.bind(this);
        this.elem = elem
        this.flag = this.elem.dataset.flag
        this.filter = new Filter(data)
        this.thead = thead
        this.tbody = tbody
        this.container = miniTable
    }

    tableSort() {
        this.filter = new Filter(data)

        let th = event.target.closest('th');
        if (!th.classList.contains('th-sortable')) return;

        const thList = this.thead.querySelectorAll('.th-sortable')
        for (const i of thList) {
            if (th!=i) i.dataset.sortMethod = 'none'
        }

        const arrowsList = this.thead.querySelectorAll('.thead-arrows')
        const arrows = th.querySelector('.thead-arrows')
        for (const arrow of arrowsList) {
            if (arrow!=arrows){
            arrow.classList = []
            arrow.classList.add('thead-arrows')
            }
        }
        let type = th.dataset.type;
        switch (th.dataset.sortMethod){
            case 'none':
                th.dataset.sortMethod = 'asc'
                arrows.classList.add('thead-arrows__asc')
                break
            case 'asc':
                th.dataset.sortMethod = 'desc'
                arrows.classList.remove('thead-arrows__asc')
                arrows.classList.add('thead-arrows__desc')
                break
            case 'desc':
                arrows.classList.remove('thead-arrows__desc')
                th.dataset.sortMethod = 'none'
                break
        }

        this.sortedList = this.filter.orderBy(type,th.dataset.sortMethod)
        this.tbody.innerHTML = this.tableCreateRow(this.sortedList)
    }

    tableCreateRow(sortedList){
        console.log(sortedList, 1)
        const manufacturerTitle = document.querySelector('.product-titles').dataset.manufacturerTitle
        const productId = document.querySelector('.product-titles').dataset.productId
        const productTitle = document.querySelector('.product-titles').dataset.productTitle
        let tbodyRows = `
                <tr class="title-row">
                    <td colspan=8>
                        <div class="title-container">
                            <div class="title-section">Запрошенный номер</div>
                            <div class="total-section">${sortedList.length}</div>
                        </div>
                    </td>
                </tr>`

        for (let data of sortedList) {
            let imgHtml = ''
            switch (data[0]) {
                case 1:
                    imgHtml = `<img src=/static/${data[4]} title="Надёжный поставщик">`
                    break
                case 2:
                    imgHtml = `<img src=/static/${data[4]} title="Дилер">`
                    break
            }
            let row = `
                        <tr>
                            <td><div class="table-manufacturer-title">${manufacturerTitle}</div></td>
                            <td><div class="table-good-number">${productId}</div></td>
                            <td>
                                <div class="table-good-info">
                                    ${imgHtml}
                                </div>
                            </td>
                            <td><div class="table-good-title">${productTitle}</div></td>
                            <td><div class="table-good-amount">${data[2]} шт.</div></td>
                            <td><div class="table-good-period">${data[3]} дн.</div></td>
                            <td><div class="table-good-price">${data[1]} ₽</div></td>
                            <td>         
                                <button class="w-full rounded-lg">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px"
                                    class="cursor-pointer fill-[#ff0000] inline-block" viewBox="0 0 512 512">
                                    <path
                                    d="M164.96 300.004h.024c.02 0 .04-.004.059-.004H437a15.003 15.003 0 0 0 14.422-10.879l60-210a15.003 15.003 0 0 0-2.445-13.152A15.006 15.006 0 0 0 497 60H130.367l-10.722-48.254A15.003 15.003 0 0 0 105 0H15C6.715 0 0 6.715 0 15s6.715 15 15 15h77.969c1.898 8.55 51.312 230.918 54.156 243.71C131.184 280.64 120 296.536 120 315c0 24.812 20.188 45 45 45h272c8.285 0 15-6.715 15-15s-6.715-15-15-15H165c-8.27 0-15-6.73-15-15 0-8.258 6.707-14.977 14.96-14.996zM477.114 90l-51.43 180H177.032l-40-180zM150 405c0 24.813 20.188 45 45 45s45-20.188 45-45-20.188-45-45-45-45 20.188-45 45zm45-15c8.27 0 15 6.73 15 15s-6.73 15-15 15-15-6.73-15-15 6.73-15 15-15zm167 15c0 24.813 20.188 45 45 45s45-20.188 45-45-20.188-45-45-45-45 20.188-45 45zm45-15c8.27 0 15 6.73 15 15s-6.73 15-15 15-15-6.73-15-15 6.73-15 15-15zm0 0"
                                    data-original="#000000"></path>
                                    </svg>
                                </button>
                        </td>
                        </tr> `
            tbodyRows += row  
        }

        return tbodyRows
    }
    miniTableCreateRow(sortedList) {
        console.log(sortedList, 2)
        let rows = ''
        for (let data of sortedList) {
            let row = `
                <div class="flex justify-between bg-gray-100 p-2">
                    <div class="">${data[2]} шт.</div>
                    <div class="">${data[3]} дн.</div>
                    <div class="font-semibold">${data[1]} ₽</div>
                    <div class="">
                        <button class="w-full rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px"
                            class="cursor-pointer fill-[#ff0000]  inline-block" viewBox="0 0 512 512">
                            <path
                            d="M164.96 300.004h.024c.02 0 .04-.004.059-.004H437a15.003 15.003 0 0 0 14.422-10.879l60-210a15.003 15.003 0 0 0-2.445-13.152A15.006 15.006 0 0 0 497 60H130.367l-10.722-48.254A15.003 15.003 0 0 0 105 0H15C6.715 0 0 6.715 0 15s6.715 15 15 15h77.969c1.898 8.55 51.312 230.918 54.156 243.71C131.184 280.64 120 296.536 120 315c0 24.812 20.188 45 45 45h272c8.285 0 15-6.715 15-15s-6.715-15-15-15H165c-8.27 0-15-6.73-15-15 0-8.258 6.707-14.977 14.96-14.996zM477.114 90l-51.43 180H177.032l-40-180zM150 405c0 24.813 20.188 45 45 45s45-20.188 45-45-20.188-45-45-45-45 20.188-45 45zm45-15c8.27 0 15 6.73 15 15s-6.73 15-15 15-15-6.73-15-15 6.73-15 15-15zm167 15c0 24.813 20.188 45 45 45s45-20.188 45-45-20.188-45-45-45-45 20.188-45 45zm45-15c8.27 0 15 6.73 15 15s-6.73 15-15 15-15-6.73-15-15 6.73-15 15-15zm0 0"
                            data-original="#000000"></path>
                        </svg>
                        </button>
                    </div>
                </div>
            `
            rows += row  
        }
        return rows
    }
    tableFilter(){
        slider.click()
        this.tbody.innerHTML = this.tableCreateRow(data)
    }

    miniTableSort(){
        slider.click()
        this.container.innerHTML = this.miniTableCreateRow(data)
    }

    updateTable(event){
        switch (this.flag){
            case 'false':
                this.tableSort()
                break
            case 'true':
                this.tableFilter()
                this.miniTableSort()
                break
        }}
}

const updateState = async (minPrice, maxPrice) => {
    const productId = document.querySelector('.product-titles').dataset.productId
    const response = await fetch(`/goods/${productId}?` + new URLSearchParams({
        'minPrice': minPrice,
        'maxPrice': maxPrice,
    }))
    const response_json = await response.json()
    data = JSON.parse(response_json['data'])
}

const tableSort = new TableUI(thead)
priceSlider()