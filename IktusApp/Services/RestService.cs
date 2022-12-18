using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using IktusApp.Models;

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
        var returnNumber = response.StatusCode.ToString();
        return returnNumber.Substring(returnNumber.Length - 1);
      }
      return "-1";
    }
  }
}
