using OpenHardwareMonitor.Hardware;
using System.Diagnostics;
using Newtonsoft.Json;

var settings = new JsonSerializerSettings { ReferenceLoopHandling = ReferenceLoopHandling.Ignore };
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

Computer c = new Computer(){
    CPUEnabled = true,
    GPUEnabled = true,
    RAMEnabled = true,
    MainboardEnabled = true,
    FanControllerEnabled = true,
    HDDEnabled = true
};

List<object> taskList = new List<object>();
Process[] processes = Process.GetProcesses();

app.Use(async (context, next) => {context.Response.Headers.Add("Content-Type", "application/json; charset=utf-8"); await next(); });
app.MapGet("/", () => "Use '/stats' or '/processes' to recieve information about them.");
app.MapGet("/clean", () => {
    c.Close();
    c.Open();
    foreach (var hardware in c.Hardware) hardware.Update();
    string serializedProcesses = JsonConvert.SerializeObject(c.Hardware, settings);
    return serializedProcesses;
});
app.MapGet("/stats", () => {
    foreach (var hardware in c.Hardware) hardware.Update();
    string serializedProcesses = JsonConvert.SerializeObject(c.Hardware, settings);
    return serializedProcesses;
});

app.MapGet("/processes", () => {
    taskList.Clear();
    processes = Process.GetProcesses();
    for (var i = 0; i < processes.Length; i++)
    {
        taskList.Add(
            new {
                id = processes[i].Id,
                processName = processes[i].ProcessName,
                mainWindowTitle = processes[i].MainWindowTitle
                // The ones down below require privileges, I can't offer this right now :/
                /*
                userProcessorTime = processes[i].UserProcessorTime,
                startTime = processes[i].StartTime.ToString(),
                mainModule = processes[i].MainModule
                */
            }
        );
    }
    string serializedProcesses = JsonConvert.SerializeObject(taskList, Formatting.Indented);
    return serializedProcesses;
});

c.Open();
app.Run();
