
const { app, BrowserWindow } = require('electron')
const { dialog } = require('electron')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win

global.Dirty = {
    is_dirty: 'true'
}

function createWindow () {
    // Create the browser window.
    win = new BrowserWindow({ width: 1600, height: 900, icon: 'icon/aurora.ico'})
    //win.setMenuBarVisibility(false)

    // and load the index.html of the app.
    win.loadFile('index.html')

    const { app, Menu } = require('electron')

    var template = [{
        label: "Aurora IR",
        submenu: [
            { label: "Quit", accelerator: "Command+Q", click: function() { app.quit(); }}
        ]}, {
        label: "Edit",
        submenu: [
            { label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:" },
            { label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:" },
            { label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:" },
        ]}
    ];

    Menu.setApplicationMenu(Menu.buildFromTemplate(template));



    // Open the DevTools
   //win.webContents.openDevTools()

    // Emitted when the window is closed.
    win.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        win = null
    })

    win.on('close', function(e){
      if(global.Dirty.is_dirty) { // if the file has not been unlocked on the server, unlock it first. needs too wait for saving to finish - hence preventDefault().
            e.preventDefault()
            win.webContents.executeJavaScript('cleanup()');
        }
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    //  if (process.platform !== 'darwin') {
        app.quit()
    //}
})

// SSL/TSL: this is the self signed certificate support
app.on('certificate-error', (event, webContents, url, error, certificate, callback) => {
    // On certificate error we disable default behaviour (stop loading the page)
    // and we then say "it is all fine - true" to the callback
    event.preventDefault();
    callback(true);
});


app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
        createWindow()
    }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

