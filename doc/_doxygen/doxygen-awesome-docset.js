/*
 * Copyright (c) 2022 TiaC Systems
 * Copyright (c) 2021 Nordic Semiconductor ASA
 * SPDX-License-Identifier: Apache-2.0
 */

window.addEventListener('DOMContentLoaded', (event) => {
  /* re-inject docset identification at a custom location */
  //let content = document.getElementById('projectnumber').innerText
  let content = document.getElementById('projectname').innerText
  let table = document.querySelector('#titlearea table');
  let cell = table.insertRow(1).insertCell(0);
  cell.innerHTML = '<div id="projectversion">' + content + '</div>';
});
