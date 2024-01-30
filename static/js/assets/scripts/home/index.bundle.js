/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/scripts/home/get_definition.js":
/*!***********************************************!*\
  !*** ./assets/scripts/home/get_definition.js ***!
  \***********************************************/
/***/ (() => {

eval("let subh = document.getElementById(\"subh\")\r\nif (document.querySelector(\"main\")) {\r\n    var main = document.querySelector(\"main\")\r\n}\r\n\r\ndocument.addEventListener(\"dblclick\", GetSelectedText)\r\n\r\nfunction GetSelectedText() {\r\n    if (window.getSelection) {\r\n        var range = window.getSelection();\r\n        var text = range.toString()\r\n    }\r\n\r\n    fetch(prde, { //post_request_definition\r\n        method: 'POST',\r\n        headers: {\r\n            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',\r\n            \"X-CSRFToken\": csrftoken\r\n        },\r\n        body: JSON.stringify(text)\r\n    }).then(async (response) => {\r\n        if (!response.ok) {\r\n            const text = await response.text()\r\n            throw new Error(text)\r\n        } else {\r\n\r\n            if (document.getElementById(\"tt\")) document.getElementById(\"tt\").remove()\r\n\r\n            if (document.getElementById(\"define\")) document.getElementById(\"define\").remove()\r\n            let div = document.createElement(\"div\")\r\n            let divContainer = document.createElement(\"div\")\r\n            divContainer.id = \"define\"\r\n            divContainer.className = \"def-container\"\r\n            let spanCross = document.createElement(\"span\")\r\n            spanCross.className = \"cross\"\r\n            let divTitle = document.createElement(\"div\")\r\n            divTitle.className = \"deft\"\r\n            divTitleContent = document.createTextNode(`${text.charAt(0).toUpperCase() + text.slice(1)}`)\r\n            divTitle.appendChild(divTitleContent)\r\n            divTitle.prepend(spanCross)\r\n            div.className = \"winbox\"\r\n            let ul = document.createElement(\"ul\")\r\n\r\n            var defs = JSON.parse(response.headers.get('definition'))\r\n            for (let i = 0; i < Object.keys(defs).length; i++) {\r\n                var li = document.createElement(\"li\")\r\n                let liContent = document.createTextNode(`${defs[i]}`)\r\n                li.appendChild(liContent)\r\n                ul.appendChild(li)\r\n            }\r\n\r\n            if (Object.keys(defs).length > 0) {\r\n                div.prepend(ul)\r\n                divContainer.prepend(div)\r\n                divContainer.prepend(divTitle)\r\n\r\n                let box = subh ? subh : main\r\n                box.prepend(divContainer)\r\n            }\r\n\r\n            var define = document.getElementById(\"define\")\r\n            spanCross.addEventListener(\"click\", function () {\r\n                define.remove()\r\n                let divtt = document.createElement(\"div\")\r\n                divtt.id = \"tt\"\r\n                divtt.className = \"dict-tt\"\r\n                divttContent = document.createTextNode(\"Get word definition\")\r\n                divtt.appendChild(divttContent)\r\n                let spantt = document.createElement(\"span\")\r\n                spantt.className = \"bg-info p-2 float-end mb-3 dict-tt-content\"\r\n                spanttContent = document.createTextNode(\"Double click on a word to get its definition\")\r\n                spantt.appendChild(spanttContent)\r\n                divtt.prepend(spantt)\r\n                main.prepend(divtt)\r\n            })\r\n        }\r\n    })\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/get_definition.js?");

/***/ }),

/***/ "./assets/scripts/home/index.js":
/*!**************************************!*\
  !*** ./assets/scripts/home/index.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./get_definition */ \"./assets/scripts/home/get_definition.js\");\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_get_definition__WEBPACK_IMPORTED_MODULE_0__);\n\r\n// import './toggle_mode'\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/scripts/home/index.js");
/******/ 	
/******/ })()
;