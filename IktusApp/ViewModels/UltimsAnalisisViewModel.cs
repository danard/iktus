using CommunityToolkit.Mvvm.ComponentModel;
using IktusApp.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IktusApp.ViewModels
{
  internal partial class UltimsAnalisisViewModel : ObservableObject
  {
    [ObservableProperty]
    List<ECG> listAnalysis;




  }
}
