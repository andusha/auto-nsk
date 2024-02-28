// import scss entry file here for app2.js
import { format } from 'date-fns';

const date = document.querySelector('[data-time]');

date.innerHTML = format(new Date(Number(date.dataset.time)*1000), "dd.MM.yyyy k:m");

