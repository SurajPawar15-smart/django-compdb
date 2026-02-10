import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DepartmentsData } from './departments-data';

describe('DepartmentsData', () => {
  let component: DepartmentsData;
  let fixture: ComponentFixture<DepartmentsData>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DepartmentsData]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DepartmentsData);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
