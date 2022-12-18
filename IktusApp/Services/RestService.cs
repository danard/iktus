using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using IktusApp.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace IktusApp.Services
{
  internal static class RestService
  {
    // Gets result of analysis as the return value
    public static async Task<string> SendNewECG(ECG item)
    {
      Uri uri = new Uri(Constants.RestUrl + Constants.endpoint);

      var ecgToBase64 = Convert.ToBase64String(File.ReadAllBytes(item.CSVFile.FullName));
      StringContent content = new StringContent(ecgToBase64);

      HttpResponseMessage response = null;
      var client = new HttpClient();
      response = await client.PostAsync(uri, content);

      if (response.IsSuccessStatusCode)
      {
        var returnValue = response.Content.ReadAsStringAsync().Result;
        var jsonNumber = JsonConvert.DeserializeObject(returnValue) as JObject;

        return jsonNumber["value"].Value<string>();
      }
      return "Error de connexió";
    }
  }
}
