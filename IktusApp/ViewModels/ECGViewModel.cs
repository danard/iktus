using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using IktusApp.Models;
using IktusApp.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IktusApp.ViewModels
{
  public partial class ECGViewModel : ObservableObject
  {
    [ObservableProperty]
    bool isLoading = false;

    [ObservableProperty]
    string lastResult = null;

    private ECG GetRandomECG()
    {
      int id = new Random().Next(1, 5);
      //var test = new FileInfo(Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, $"Resources/InputData/ECG{id}.pdf"));
      var test = new FileInfo(Path.Combine("C:\\Users\\ardevold\\Downloads\\Ictus Files\\EGC Files\\" + $"ecg{id}.pdf"));

      return new ECG
        (
        DateTime.Now,
        test,
        "FitBit"
        );
    }

    [RelayCommand]
    public async Task SendNewAnalysis()
    {
      IsLoading = true;
      try
      {
        Thread.Sleep(2000);
        LastResult = await RestService.SendNewECG(GetRandomECG());
      }
      finally
      {
        IsLoading = false;
      }
    }
  }
}
