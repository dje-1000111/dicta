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

/***/ "./assets/scripts/base/index.js":
/*!**************************************!*\
  !*** ./assets/scripts/base/index.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _toggle_mode__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./toggle_mode */ \"./assets/scripts/base/toggle_mode.js\");\n/* harmony import */ var _toggle_mode__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_toggle_mode__WEBPACK_IMPORTED_MODULE_0__);\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/base/index.js?");

/***/ }),

/***/ "./assets/scripts/base/toggle_mode.js":
/*!********************************************!*\
  !*** ./assets/scripts/base/toggle_mode.js ***!
  \********************************************/
/***/ (() => {

eval("// if (document.getElementById(\"bas\")) {\r\n//     var bas = document.getElementById(\"bas\")\r\n// }\r\n\r\nconst ligbtn = document.getElementById(\"ligbtn\")\r\nconst darkBtn = document.getElementById(\"darkbtn\")\r\n\r\n\r\nvar darkMode;\r\nif (localStorage.getItem('dark-mode')) {\r\n    darkMode = localStorage.getItem('dark-mode');\r\n} else {\r\n    darkMode = 'light';\r\n}\r\nlocalStorage.setItem('dark-mode', darkMode);\r\n\r\ntables = document.querySelectorAll(\"table\")\r\n\r\nif (document.getElementById(\"hcontainer\")) {\r\n    var hcontainer = document.getElementById(\"hcontainer\")\r\n}\r\n\r\nif (document.getElementById(\"tcontainer\")) {\r\n    var tcontainer = document.getElementById(\"tcontainer\")\r\n}\r\n\r\n\r\nif (document.getElementById(\"embvid\")) {\r\n    var embvid = document.getElementById(\"embvid\")\r\n}\r\n\r\nif (document.getElementById(\"text-area\")) {\r\n    var textarea = document.getElementById(\"text-area\")\r\n}\r\n\r\nif (document.getElementById(\"subh\")) {\r\n    var subh = document.getElementById(\"subh\")\r\n}\r\n\r\nif (document.getElementById(\"bonus-txt\")) {\r\n    var bonusTxt = document.getElementById(\"bonus-txt\")\r\n}\r\n\r\nif (document.getElementById(\"bonus-container\")) {\r\n    var bonusContainer = document.getElementById(\"bonus-container\")\r\n}\r\n\r\nif (document.getElementById(\"prof\")) {\r\n    var prof = document.getElementById(\"prof\")\r\n}\r\n\r\nif (document.getElementById(\"profile-container\")) {\r\n    var profileContainer = document.getElementById(\"profile-container\")\r\n}\r\n\r\nif (document.querySelector(\"main\")) {\r\n    var main = document.querySelector(\"main\")\r\n}\r\n\r\nif (document.getElementById(\"counter-cont\")) {\r\n    var counterCont = document.getElementById(\"counter-cont\")\r\n}\r\n\r\n\r\n\r\nif (localStorage.getItem('dark-mode') == 'dark') {\r\n    if (hcontainer) {\r\n        hcontainer.classList.toggle(\"dark-mode\");\r\n        hcontainer.classList.add(\"hdark\");\r\n        // hcontainer.classList.remove(\"light\");\r\n    }\r\n    if (tcontainer) {\r\n        tcontainer.classList.toggle(\"dark-mode\");\r\n    }\r\n\r\n\r\n    if (subh) {\r\n        // subh.classList.toggle(\"dark-mode\");\r\n        subh.classList.add(\"dark\");\r\n        subh.classList.remove(\"light\");\r\n\r\n        embvid.classList.add(\"dark\");\r\n        embvid.classList.remove(\"light\");\r\n        textarea.classList.add(\"dark\");\r\n        textarea.classList.remove(\"light\");\r\n        bonusTxt.classList.add(\"dark\");\r\n        bonusTxt.classList.remove(\"light\");\r\n\r\n        bonusContainer.classList.add(\"dark-bonus-cont\");\r\n        bonusContainer.classList.remove(\"light-bonus-cont\");\r\n\r\n        counterCont.classList.add(\"dark-counter-cont\");\r\n        counterCont.classList.remove(\"light-counter-cont\");\r\n\r\n    }\r\n\r\n    if (main) {\r\n        main.classList.add(\"dark\");\r\n        main.classList.remove(\"light\");\r\n    }\r\n    if (prof) {\r\n        profileContainer.classList.add(\"dark-profile-cont\");\r\n        profileContainer.classList.remove(\"light-profile-cont\");\r\n    }\r\n    darkBtn.hidden = true\r\n    ligbtn.hidden = false\r\n    tables.forEach(table => {\r\n        // table.classList.remove(\"table-light\")\r\n        table.classList.add(\"table-dark\")\r\n    });\r\n\r\n    // if (document.getElementById(\"bas\")) {\r\n    //     bas.classList.remove(\"bg-light\")\r\n    //     bas.classList.add(\"bg-dark-subtle\")\r\n    // }\r\n}\r\n\r\ndarkBtn.addEventListener(\"click\", function (e) {\r\n    if (e.target.hidden === false) {\r\n        darkBtn.hidden = true\r\n        ligbtn.hidden = false\r\n        if (hcontainer) {\r\n            hcontainer.classList.toggle(\"dark-mode\");\r\n            hcontainer.classList.add(\"hdark\");\r\n            // hcontainer.classList.remove(\"light\");\r\n        }\r\n        if (tcontainer) {\r\n            tcontainer.classList.toggle(\"dark-mode\");\r\n        }\r\n        if (subh) {\r\n            subh.classList.add(\"dark\");\r\n            subh.classList.remove(\"light\");\r\n            embvid.classList.add(\"dark\");\r\n            embvid.classList.remove(\"light\");\r\n            textarea.classList.add(\"dark\");\r\n            textarea.classList.remove(\"light\");\r\n            bonusTxt.classList.add(\"dark\");\r\n            bonusTxt.classList.remove(\"light\");\r\n\r\n            bonusContainer.classList.add(\"dark-bonus-cont\");\r\n            bonusContainer.classList.remove(\"light-bonus-cont\");\r\n            counterCont.classList.add(\"dark-counter-cont\");\r\n            counterCont.classList.remove(\"light-counter-cont\");\r\n        }\r\n        if (main) {\r\n            main.classList.add(\"dark\");\r\n            main.classList.remove(\"light\");\r\n\r\n        }\r\n        if (prof) {\r\n            profileContainer.classList.add(\"dark-profile-cont\");\r\n            profileContainer.classList.remove(\"light-profile-cont\");\r\n        }\r\n        tables.forEach(table => {\r\n            // table.classList.remove(\"table-light\")\r\n            table.classList.add(\"table-dark\")\r\n        });\r\n\r\n        // if (document.getElementById(\"bas\")) {\r\n        //     bas.classList.remove(\"bg-light\")\r\n        //     bas.classList.add(\"bg-dark-subtle\")\r\n        // }\r\n        localStorage.setItem('dark-mode', 'dark');\r\n    }\r\n});\r\n\r\nligbtn.addEventListener(\"click\", function (e) {\r\n    if (e.target.hidden === false) {\r\n        ligbtn.hidden = true\r\n        darkBtn.hidden = false\r\n        if (hcontainer) {\r\n            hcontainer.classList.toggle(\"dark-mode\");\r\n            // hcontainer.classList.add(\"light\");\r\n            hcontainer.classList.remove(\"hdark\");\r\n        }\r\n        if (tcontainer) {\r\n            tcontainer.classList.toggle(\"dark-mode\");\r\n        }\r\n        if (subh) {\r\n            subh.classList.add(\"light\");\r\n            subh.classList.remove(\"dark\");\r\n            embvid.classList.add(\"light\");\r\n            embvid.classList.remove(\"dark\");\r\n            textarea.classList.add(\"light\");\r\n            textarea.classList.remove(\"dark\");\r\n            bonusTxt.classList.add(\"light\");\r\n            bonusTxt.classList.remove(\"dark\");\r\n\r\n            bonusContainer.classList.add(\"light-bonus-cont\");\r\n            bonusContainer.classList.remove(\"dark-bonus-cont\");\r\n            counterCont.classList.add(\"light-counter-cont\");\r\n            counterCont.classList.remove(\"dark-counter-cont\");\r\n        }\r\n        if (main) {\r\n            main.classList.add(\"light\");\r\n            main.classList.remove(\"dark\");\r\n\r\n        }\r\n\r\n        if (prof) {\r\n            profileContainer.classList.add(\"light-profile-cont\");\r\n            profileContainer.classList.remove(\"dark-profile-cont\");\r\n        }\r\n\r\n        tables.forEach(table => {\r\n            table.classList.remove(\"table-dark\")\r\n            // table.classList.add(\"table-light\")\r\n        });\r\n\r\n        // if (document.getElementById(\"bas\")) {\r\n        //     bas.classList.remove(\"bg-dark-subtle\")\r\n        //     bas.classList.add(\"bg-light\")\r\n        // }\r\n        localStorage.setItem('dark-mode', 'light');\r\n    }\r\n});\r\n\r\n\r\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/base/toggle_mode.js?");

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
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/scripts/base/index.js");
/******/ 	
/******/ })()
;