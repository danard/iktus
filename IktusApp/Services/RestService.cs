using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using IktusApp.Models;

namespace IktusApp.Services
{
  internal class RestService
  {
    private HttpClient client;

    public async Task SendNewECG(ECG item, bool isNewItem = false)
    {
      Uri uri = new Uri(string.Format(Constants.RestUrl, string.Empty));

      string json = "test";
      StringContent content = new StringContent(json, Encoding.UTF8, "application/json");

      HttpResponseMessage response = null;
      if (isNewItem)
      {
        response = await client.PostAsync(uri, content);
      }

      if (response.IsSuccessStatusCode)
      {
        //Debug.WriteLine(@"\tTodoItem successfully saved.");
      }}
  }
}
