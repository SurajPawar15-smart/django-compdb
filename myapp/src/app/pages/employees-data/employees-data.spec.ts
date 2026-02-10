import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployeesData } from './employees-data';

describe('EmployeesData', () => {
  let component: EmployeesData;
  let fixture: ComponentFixture<EmployeesData>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployeesData]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployeesData);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
